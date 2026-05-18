from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from .cli import parse_args
from .window import PlayerWindow


def main() -> int:
    options = parse_args(sys.argv[1:])
    app = QApplication(sys.argv)
    app.setApplicationName("Qt-Kurarin")

    window = PlayerWindow(frame_style=options.frame_style)
    window.show()
    window.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
