from __future__ import annotations

import sys
from collections import deque
from pathlib import Path
from threading import Lock

from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QGuiApplication, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

from .frame_style import content_clip_path, draw_frame
from .animation import Movement, PlaybackSnapshot, SpriteFrame
from .parser import parse_script
from .player import AudioClock
from .sprite import RenderSprite, build_render_sprites


def resolve_app_icon_path(package_dir: Path) -> Path | None:
    logo_dir = package_dir / "resources" / "logo"
    candidates: list[Path] = []
    if sys.platform == "darwin":
        candidates.extend(
            [
                logo_dir / "logo.icns",
                logo_dir / "logo_macos_512.png",
                logo_dir / "logo.png",
            ]
        )
    elif sys.platform.startswith("win"):
        candidates.extend(
            [
                logo_dir / "logo.ico",
                logo_dir / "logo.png",
            ]
        )
    else:
        candidates.extend(
            [
                logo_dir / "logo.png",
                logo_dir / "logo.ico",
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


class PlayerWindow(QWidget):
    def __init__(
        self,
        frame_style: str = "none",
        verbose: bool = False,
        loudness: int = 100,
        hide_taskbar: bool = False,
    ) -> None:
        super().__init__(None)
        self.hide_taskbar = hide_taskbar
        self._apply_window_flags()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        screen = QGuiApplication.primaryScreen()

        if screen is not None:
            self.setGeometry(screen.geometry())

        package_dir = Path(__file__).resolve().parent
        self.package_dir = package_dir
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
        self._recent_events: deque[str] = deque(maxlen=12)
        self._snapshot_lock = Lock()
        self._snapshot = PlaybackSnapshot(
            time_ms=0,
            total_duration=0,
            frame_style=frame_style,
            loudness=loudness,
            total_sprites=0,
        )

        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self._tick)

        self._setup_window_icon()
        self._load_scene()
        self._ensure_linux_desktop_file()

    def _apply_window_flags(self) -> None:
        if self.hide_taskbar:
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint
                | Qt.WindowType.WindowStaysOnTopHint
                | Qt.WindowType.Tool
            )
        else:
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
            )

    def _setup_window_icon(self) -> None:
        icon_path = resolve_app_icon_path(self.package_dir)
        if icon_path is not None:
            self.setWindowIcon(QIcon(str(icon_path)))
        self.setWindowTitle("Qt-Kurarin")

    def _ensure_linux_desktop_file(self) -> None:
        if not sys.platform.startswith("linux"):
            return
        icon_path = self.resources_dir / "logo" / "logo.png"
        if not icon_path.exists():
            return
        desktop_dir = Path.home() / ".local" / "share" / "applications"
        desktop_path = desktop_dir / "qt-kurarin.desktop"
        if desktop_path.exists():
            return
        try:
            desktop_dir.mkdir(parents=True, exist_ok=True)
            desktop_path.write_text(
                "[Desktop Entry]\n"
                f"Type=Application\n"
                f"Name=Qt-Kurarin\n"
                f"Icon={icon_path.resolve()}\n"
                f"Exec={sys.executable} -m qt_kurarin.main\n"
                f"Terminal=false\n"
                f"Categories=AudioVideo;\n",
                encoding="utf-8",
            )
        except OSError:
            pass

    def shutdown(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
        self.clock.stop()
        self.close()

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self.shutdown()
        QApplication.quit()
        event.accept()

    def _load_scene(self) -> None:
        definitions, self.max_time = parse_script(self.script_path)
        pixmaps = self._load_pixmaps(
            {definition.resource_name for definition in definitions}
        )
        self.render_sprites = build_render_sprites(definitions, pixmaps)
        with self._snapshot_lock:
            self._snapshot.total_sprites = len(self.render_sprites)
            self._snapshot.total_duration = self.max_time

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
                total_duration=self._snapshot.total_duration,
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
                        status=frame.status,
                    )
                    for frame in self._snapshot.visible_sprites
                ],
                recent_events=list(self._snapshot.recent_events),
                scene_summary=self._snapshot.scene_summary,
                total_sprites=self._snapshot.total_sprites,
                moving_count=self._snapshot.moving_count,
                fading_count=self._snapshot.fading_count,
                scaling_count=self._snapshot.scaling_count,
                holding_count=self._snapshot.holding_count,
            )

    def _update_snapshot(self, elapsed: int, visible_frames: list[SpriteFrame]) -> None:
        visible_frames = sorted(
            visible_frames,
            key=lambda frame: (
                frame.width * frame.height * frame.opacity,
                frame.opacity,
            ),
            reverse=True,
        )
        moving_count = sum("moving" in frame.status for frame in visible_frames)
        fading_count = sum("fading" in frame.status for frame in visible_frames)
        scaling_count = sum("scaling" in frame.status for frame in visible_frames)
        holding_count = sum(frame.status == "holding" for frame in visible_frames)
        with self._snapshot_lock:
            self._snapshot.time_ms = elapsed
            self._snapshot.visible_sprites = visible_frames
            self._snapshot.recent_events = list(self._recent_events)
            self._snapshot.scene_summary = self._make_scene_summary(visible_frames)
            self._snapshot.moving_count = moving_count
            self._snapshot.fading_count = fading_count
            self._snapshot.scaling_count = scaling_count
            self._snapshot.holding_count = holding_count

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

    def _emit_event(self, time_ms: int, message: str) -> None:
        line = f"[{time_ms:6d} ms] {message}"
        self._recent_events.append(line)
        if self.verbose:
            print(line, flush=True)

    def _make_scene_summary(self, visible_frames: list[SpriteFrame]) -> str:
        if not visible_frames:
            return "Stage is empty right now."
        lead = max(
            visible_frames,
            key=lambda frame: frame.width * frame.height * max(frame.opacity, 0.001),
        )
        active_bits = []
        moving = sum("moving" in frame.status for frame in visible_frames)
        fading = sum("fading" in frame.status for frame in visible_frames)
        scaling = sum("scaling" in frame.status for frame in visible_frames)
        if moving:
            active_bits.append(f"{moving} moving")
        if fading:
            active_bits.append(f"{fading} fading")
        if scaling:
            active_bits.append(f"{scaling} scaling")
        if not active_bits:
            active_bits.append("quiet hold")
        return (
            f"Lead: {lead.resource_name} ({lead.status}). "
            f"Scene: {len(visible_frames)} visible sprites, {', '.join(active_bits)}."
        )

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
                self._emit_event(elapsed, f"show {self._log_sprite_frame(frame)}")
            self._last_verbose_time = elapsed
            self._last_visible_resources = current_visible_resources
            self._last_visible_frames = dict(visible_by_resource)
            return

        last_time = self._last_verbose_time

        for resource_name in sorted(
            current_visible_resources - self._last_visible_resources
        ):
            frame = visible_by_resource[resource_name]
            self._emit_event(elapsed, f"show {self._log_sprite_frame(frame)}")

        for resource_name in sorted(
            self._last_visible_resources - current_visible_resources
        ):
            frame = self._last_visible_frames.get(resource_name)
            if frame is not None:
                self._emit_event(elapsed, f"hide {self._log_sprite_frame(frame)}")
            else:
                self._emit_event(elapsed, f"hide {resource_name}")

        for sprite in self.render_sprites:
            for movement in sprite.definition.movements:
                if last_time < movement.time_start <= elapsed:
                    frame = sprite.sample_frame(
                        movement.time_start, global_scale, offset_x, offset_y
                    )
                    detail = self._movement_detail(movement)
                    suffix = f" {detail}" if detail else ""
                    if movement.is_instant:
                        if frame is not None:
                            self._emit_event(
                                movement.time_start,
                                f"{self._movement_label(movement)} {self._log_sprite_frame(frame)}{suffix}",
                            )
                        else:
                            self._emit_event(
                                movement.time_start,
                                f"{self._movement_label(movement)} {sprite.definition.resource_name}{suffix}",
                            )
                    else:
                        if frame is not None:
                            self._emit_event(
                                movement.time_start,
                                f"{self._movement_label(movement)}-start {self._log_sprite_frame(frame)}{suffix}",
                            )
                        else:
                            self._emit_event(
                                movement.time_start,
                                f"{self._movement_label(movement)}-start {sprite.definition.resource_name}{suffix}",
                            )
                if not movement.is_instant and last_time < movement.time_end <= elapsed:
                    frame = sprite.sample_frame(
                        movement.time_end, global_scale, offset_x, offset_y
                    )
                    detail = self._movement_detail(movement)
                    suffix = f" {detail}" if detail else ""
                    if frame is not None:
                        self._emit_event(
                            movement.time_end,
                            f"{self._movement_label(movement)}-end {self._log_sprite_frame(frame)}{suffix}",
                        )
                    else:
                        self._emit_event(
                            movement.time_end,
                            f"{self._movement_label(movement)}-end {sprite.definition.resource_name}{suffix}",
                        )

        self._last_verbose_time = elapsed
        self._last_visible_resources = current_visible_resources
        self._last_visible_frames = dict(visible_by_resource)
