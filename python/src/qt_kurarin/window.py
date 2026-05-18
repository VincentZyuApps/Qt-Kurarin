from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QGuiApplication, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

from .frame_style import content_clip_path, draw_frame
from .animation import SpriteFrame
from .parser import parse_script
from .player import AudioClock
from .sprite import RenderSprite, build_render_sprites


class PlayerWindow(QWidget):
    def __init__(self, frame_style: str = "none", verbose: bool = False) -> None:
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

        self.render_sprites: list[RenderSprite] = []
        self.max_time = 0
        self.clock = AudioClock(self.audio_path)
        self._last_verbose_time = -1

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
        if self.verbose:
            self._log_verbose_frame(elapsed)
        self.update()

    def _log_verbose_frame(self, elapsed: int) -> None:
        if elapsed == self._last_verbose_time:
            return
        self._last_verbose_time = elapsed
        print(f"[{elapsed:6d} ms] frame", flush=True)

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

        for sprite in self.render_sprites:
            sampled = sprite.evaluate(elapsed, global_scale, offset_x, offset_y)
            if sampled is None:
                continue
            target_rect, opacity, frame = sampled
            if self.verbose:
                self._log_sprite_frame(frame, target_rect)
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

        painter.end()

    def _log_sprite_frame(self, frame: SpriteFrame, target_rect: QRectF) -> None:
        print(
            f"  {frame.resource_name} x={frame.x:.1f} y={frame.y:.1f} "
            f"w={target_rect.width():.1f} h={target_rect.height():.1f} "
            f"opacity={frame.opacity:.3f} scale={frame.scale:.3f}",
            flush=True,
        )
