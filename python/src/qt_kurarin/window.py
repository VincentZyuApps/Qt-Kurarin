from __future__ import annotations

from pathlib import Path
from threading import Lock

from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QGuiApplication, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

from .frame_style import content_clip_path, draw_frame
from .animation import Movement, PlaybackSnapshot, SpriteFrame
from .parser import parse_script
from .player import AudioClock
from .sprite import RenderSprite, build_render_sprites


class PlayerWindow(QWidget):
    def __init__(self, frame_style: str = "none", verbose: bool = False, loudness: int = 100) -> None:
        flags = (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        super().__init__(None, flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            self.setGeometry(screen.geometry())

        package_dir = Path(__file__).resolve().parent
        self.script_path = package_dir / "data" / "script.txt"
        self.resources_dir = package_dir / "resources"
        self.audio_path = self.resources_dir / "audio.mp3"
        self.frame_style = frame_style
        self.verbose = verbose
        self.loudness = loudness

        self.render_sprites: list[RenderSprite] = []
        self.max_time = 0
        self.clock = AudioClock(self.audio_path, loudness=loudness)
        self._last_verbose_time: int | None = None
        self._last_visible_resources: set[str] = set()
        self._last_visible_frames: dict[str, SpriteFrame] = {}
        self._snapshot_lock = Lock()
        self._snapshot = PlaybackSnapshot(
            time_ms=0,
            frame_style=frame_style,
            loudness=loudness,
            total_sprites=0,
        )

        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self._tick)

        self._load_scene()

    def shutdown(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
        self.clock.stop()
        self.close()

    def _load_scene(self) -> None:
        definitions, self.max_time = parse_script(self.script_path)
        pixmaps = self._load_pixmaps({definition.resource_name for definition in definitions})
        self.render_sprites = build_render_sprites(definitions, pixmaps)
        with self._snapshot_lock:
            self._snapshot.total_sprites = len(self.render_sprites)

    def _load_pixmaps(self, names: set[str]) -> dict[str, QPixmap]:
        pixmaps: dict[str, QPixmap] = {}
        for name in names:
            image_path = self.resources_dir / name
            pixmap = QPixmap(str(image_path))
            if pixmap.isNull():
                continue
            pixmaps[name] = pixmap
        return pixmaps

    def start(self) -> None:
        self.clock.start()
        self.timer.start()

    def _tick(self) -> None:
        elapsed = self.clock.position()
        if elapsed > self.max_time + 1000:
            self.shutdown()
            QApplication.quit()
            return
        self.update()

    def get_snapshot(self) -> PlaybackSnapshot:
        with self._snapshot_lock:
            return PlaybackSnapshot(
                time_ms=self._snapshot.time_ms,
                frame_style=self._snapshot.frame_style,
                loudness=self._snapshot.loudness,
                visible_sprites=[
                    SpriteFrame(
                        resource_name=frame.resource_name,
                        time_ms=frame.time_ms,
                        x=frame.x,
                        y=frame.y,
                        width=frame.width,
                        height=frame.height,
                        opacity=frame.opacity,
                        scale=frame.scale,
                        visible=frame.visible,
                    )
                    for frame in self._snapshot.visible_sprites
                ],
                total_sprites=self._snapshot.total_sprites,
            )

    def _update_snapshot(self, elapsed: int, visible_frames: list[SpriteFrame]) -> None:
        with self._snapshot_lock:
            self._snapshot.time_ms = elapsed
            self._snapshot.visible_sprites = visible_frames

    def paintEvent(self, event) -> None:  # type: ignore[override]
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        height = self.height() - 180
        width = self.width()
        global_scale = height / 480.0
        offset_y = 90.0
        offset_x = (width - 640.0 * global_scale) / 2.0
        elapsed = self.clock.position()
        visible_frames: list[SpriteFrame] = []
        visible_by_resource: dict[str, SpriteFrame] = {}

        for sprite in self.render_sprites:
            sampled = sprite.evaluate(elapsed, global_scale, offset_x, offset_y)
            if sampled is None:
                continue
            target_rect, opacity, frame = sampled
            visible_frames.append(frame)
            visible_by_resource[frame.resource_name] = frame
            painter.setOpacity(opacity)
            content_rect = draw_frame(
                painter=painter,
                content_rect=target_rect,
                frame_style=self.frame_style,
                title=sprite.definition.resource_name.replace(".png", ""),
                opacity=opacity,
            )
            clip_path = content_clip_path(content_rect, self.frame_style)
            painter.save()
            if clip_path is not None:
                painter.setClipPath(clip_path)
            painter.drawPixmap(content_rect.toRect(), sprite.pixmap)
            painter.restore()

        if self.verbose:
            self._log_verbose_events(
                elapsed=elapsed,
                global_scale=global_scale,
                offset_x=offset_x,
                offset_y=offset_y,
                visible_by_resource=visible_by_resource,
            )
        self._update_snapshot(elapsed, visible_frames)
        painter.end()

    def _log_sprite_frame(self, frame: SpriteFrame) -> str:
        return (
            f"{frame.resource_name} "
            f"xy=({frame.x:.1f}, {frame.y:.1f}) "
            f"size=({frame.width:.1f}x{frame.height:.1f}) "
            f"opacity={frame.opacity:.3f} scale={frame.scale:.3f}"
        )

    def _movement_label(self, movement: Movement) -> str:
        return {
            "M": "move",
            "MX": "move-x",
            "MY": "move-y",
            "F": "fade",
            "S": "scale",
        }.get(movement.type, movement.type.lower())

    def _movement_detail(self, movement: Movement) -> str:
        if movement.type == "F":
            return f"opacity {movement.move_from:.3f}->{movement.move_end:.3f}"
        if movement.type == "S":
            return f"scale {movement.move_from:.3f}->{movement.move_end:.3f}"
        if movement.type == "MX":
            return f"x {movement.move_from:.1f}->{movement.move_end:.1f}"
        if movement.type == "MY":
            return f"y {movement.move_from:.1f}->{movement.move_end:.1f}"
        if movement.type == "M":
            return "xy motion"
        return ""

    def _log_verbose_events(
        self,
        elapsed: int,
        global_scale: float,
        offset_x: float,
        offset_y: float,
        visible_by_resource: dict[str, SpriteFrame],
    ) -> None:
        if self._last_verbose_time == elapsed:
            return

        current_visible_resources = set(visible_by_resource)
        if self._last_verbose_time is None:
            for frame in visible_by_resource.values():
                print(f"[{elapsed:6d} ms] show {self._log_sprite_frame(frame)}", flush=True)
            self._last_verbose_time = elapsed
            self._last_visible_resources = current_visible_resources
            self._last_visible_frames = dict(visible_by_resource)
            return

        last_time = self._last_verbose_time

        for resource_name in sorted(current_visible_resources - self._last_visible_resources):
            frame = visible_by_resource[resource_name]
            print(f"[{elapsed:6d} ms] show {self._log_sprite_frame(frame)}", flush=True)

        for resource_name in sorted(self._last_visible_resources - current_visible_resources):
            frame = self._last_visible_frames.get(resource_name)
            if frame is not None:
                print(f"[{elapsed:6d} ms] hide {self._log_sprite_frame(frame)}", flush=True)
            else:
                print(f"[{elapsed:6d} ms] hide {resource_name}", flush=True)

        for sprite in self.render_sprites:
            for movement in sprite.definition.movements:
                if last_time < movement.time_start <= elapsed:
                    frame = sprite.sample_frame(movement.time_start, global_scale, offset_x, offset_y)
                    detail = self._movement_detail(movement)
                    suffix = f" {detail}" if detail else ""
                    if movement.is_instant:
                        if frame is not None:
                            print(
                                f"[{movement.time_start:6d} ms] {self._movement_label(movement)} {self._log_sprite_frame(frame)}{suffix}",
                                flush=True,
                            )
                        else:
                            print(
                                f"[{movement.time_start:6d} ms] {self._movement_label(movement)} {sprite.definition.resource_name}{suffix}",
                                flush=True,
                            )
                    else:
                        if frame is not None:
                            print(
                                f"[{movement.time_start:6d} ms] {self._movement_label(movement)}-start {self._log_sprite_frame(frame)}{suffix}",
                                flush=True,
                            )
                        else:
                            print(
                                f"[{movement.time_start:6d} ms] {self._movement_label(movement)}-start {sprite.definition.resource_name}{suffix}",
                                flush=True,
                            )
                if not movement.is_instant and last_time < movement.time_end <= elapsed:
                    frame = sprite.sample_frame(movement.time_end, global_scale, offset_x, offset_y)
                    detail = self._movement_detail(movement)
                    suffix = f" {detail}" if detail else ""
                    if frame is not None:
                        print(
                            f"[{movement.time_end:6d} ms] {self._movement_label(movement)}-end {self._log_sprite_frame(frame)}{suffix}",
                            flush=True,
                        )
                    else:
                        print(
                            f"[{movement.time_end:6d} ms] {self._movement_label(movement)}-end {sprite.definition.resource_name}{suffix}",
                            flush=True,
                        )

        self._last_verbose_time = elapsed
        self._last_visible_resources = current_visible_resources
        self._last_visible_frames = dict(visible_by_resource)
