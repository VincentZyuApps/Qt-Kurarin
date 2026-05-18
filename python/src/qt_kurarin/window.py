from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QGuiApplication, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

from .parser import parse_script
from .player import AudioClock
from .sprite import RenderSprite, build_render_sprites


class PlayerWindow(QWidget):
    def __init__(self) -> None:
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

        base_dir = Path(__file__).resolve().parents[2]
        self.script_path = base_dir / "data" / "script.txt"
        self.resources_dir = base_dir / "resources"
        self.audio_path = self.resources_dir / "audio.mp3"

        self.render_sprites: list[RenderSprite] = []
        self.max_time = 0
        self.clock = AudioClock(self.audio_path)

        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self._tick)

        self._load_scene()

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
            self.timer.stop()
            self.clock.stop()
            QApplication.quit()
            return
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

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
            target_rect, opacity = sampled
            painter.setOpacity(opacity)
            painter.drawPixmap(target_rect.toRect(), sprite.pixmap)

        painter.end()
