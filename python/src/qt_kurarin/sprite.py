from __future__ import annotations

import math
from dataclasses import dataclass

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPixmap

from .animation import Movement, SpriteDefinition, SpriteFrame, SpriteState, SENTINEL_END
from .easing import get_easing


def _anchor_offset(size: float) -> float:
    return -size / 2


@dataclass(slots=True)
class RenderSprite:
    definition: SpriteDefinition
    pixmap: QPixmap

    def evaluate(self, time_ms: int, global_scale: float, offset_x: float, offset_y: float) -> tuple[QRectF, float, SpriteFrame] | None:
        frame = self.sample_frame(time_ms, global_scale, offset_x, offset_y)
        if frame is None:
            return None
        return QRectF(frame.x, frame.y, frame.width, frame.height), frame.opacity, frame

    def sample_frame(self, time_ms: int, global_scale: float, offset_x: float, offset_y: float) -> SpriteFrame | None:
        if self.pixmap.isNull():
            return None
        if self.definition.movements and time_ms < self.definition.movements[0].time_start:
            return None

        state = SpriteState(
            x=self.definition.x,
            y=self.definition.y,
            opacity=1.0,
            scale=1.0,
        )

        for movement in self.definition.movements:
            if movement.time_start > time_ms:
                break
            self._apply_movement(state, movement, time_ms)

        if state.opacity <= 0.001:
            return None

        width = self.pixmap.width() * state.scale * global_scale
        height = self.pixmap.height() * state.scale * global_scale
        if width <= 0 or height <= 0:
            return None

        x = state.x * global_scale + offset_x + _anchor_offset(width)
        y = state.y * global_scale + offset_y + _anchor_offset(height)
        status = self._describe_status(time_ms)
        frame = SpriteFrame(
            resource_name=self.definition.resource_name,
            time_ms=time_ms,
            x=x,
            y=y,
            width=width,
            height=height,
            opacity=max(0.0, min(1.0, state.opacity)),
            scale=state.scale,
            visible=True,
            status=status,
        )
        return frame

    def _describe_status(self, time_ms: int) -> str:
        labels: list[str] = []
        for movement in self.definition.movements:
            if movement.is_instant:
                continue
            if movement.time_start <= time_ms < movement.time_end:
                if movement.type in {"M", "MX", "MY"} and "moving" not in labels:
                    labels.append("moving")
                elif movement.type == "F":
                    labels.append("fading in" if movement.move_end >= movement.move_from else "fading out")
                elif movement.type == "S":
                    labels.append("scaling up" if movement.move_end >= movement.move_from else "scaling down")
        if not labels:
            return "holding"
        return ", ".join(labels)

    def _apply_movement(self, state: SpriteState, movement: Movement, time_ms: int) -> None:
        if movement.is_instant or movement.time_end == SENTINEL_END:
            self._apply_value(state, movement, movement.move_from, movement.sub_value, movement.move_end)
            return

        if time_ms >= movement.time_end:
            self._apply_value(state, movement, movement.move_end, movement.sub_value, movement.sub_value2)
            return

        duration = movement.time_end - movement.time_start
        if duration <= 0:
            self._apply_value(state, movement, movement.move_end, movement.sub_value, movement.sub_value2)
            return

        progress = (time_ms - movement.time_start) / duration
        progress = get_easing(movement.easing, progress)

        match movement.type:
            case "M":
                from_y = movement.move_end
                to_x = movement.sub_value if not math.isnan(movement.sub_value) else movement.move_from
                to_y = movement.sub_value2 if not math.isnan(movement.sub_value2) else movement.move_end
                state.x = movement.move_from + (to_x - movement.move_from) * progress
                state.y = from_y + (to_y - from_y) * progress
            case "MX":
                state.x = movement.move_from + (movement.move_end - movement.move_from) * progress
                if not math.isnan(movement.sub_value):
                    state.y = movement.sub_value
            case "MY":
                if not math.isnan(movement.sub_value):
                    state.x = movement.sub_value
                state.y = movement.move_from + (movement.move_end - movement.move_from) * progress
            case "F":
                state.opacity = movement.move_from + (movement.move_end - movement.move_from) * progress
            case "S":
                state.scale = movement.move_from + (movement.move_end - movement.move_from) * progress

    def _apply_value(
        self,
        state: SpriteState,
        movement: Movement,
        value: float,
        sub_value: float,
        sub_value2: float,
    ) -> None:
        match movement.type:
            case "M":
                state.x = movement.move_from
                state.y = movement.move_end
                if not math.isnan(sub_value):
                    state.x = sub_value
                if not math.isnan(sub_value2):
                    state.y = sub_value2
            case "MX":
                state.x = value
                if not math.isnan(sub_value):
                    state.y = sub_value
            case "MY":
                if not math.isnan(sub_value):
                    state.x = sub_value
                state.y = value
            case "F":
                state.opacity = value
            case "S":
                state.scale = value


def build_render_sprites(definitions: list[SpriteDefinition], pixmaps: dict[str, QPixmap]) -> list[RenderSprite]:
    sprites: list[RenderSprite] = []
    for definition in definitions:
        pixmap = pixmaps.get(definition.resource_name)
        if pixmap is None:
            continue
        sprites.append(RenderSprite(definition=definition, pixmap=pixmap))
    return sprites
