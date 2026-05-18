from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QElapsedTimer, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer


class AudioClock:
    def __init__(self, audio_path: Path) -> None:
        self.audio_path = audio_path
        self.elapsed = QElapsedTimer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(1.0)
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self._audio_loaded = False

        if audio_path.is_file():
            self.media_player.setSource(QUrl.fromLocalFile(str(audio_path)))
            self._audio_loaded = True

    def start(self) -> None:
        self.elapsed.start()
        if self._audio_loaded:
            self.media_player.play()

    def position(self) -> int:
        if self._audio_loaded:
            media_position = self.media_player.position()
            if media_position > 0:
                return media_position
        return self.elapsed.elapsed()

    def stop(self) -> None:
        if self._audio_loaded:
            self.media_player.stop()
