from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from .window import PlayerWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Qt-Kurarin")

    window = PlayerWindow()
    window.show()
    window.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
