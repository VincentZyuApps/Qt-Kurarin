from __future__ import annotations

import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from .cli import parse_args
from .window import PlayerWindow


ANSI_GREEN = "\033[92m"
ANSI_RESET = "\033[0m"


def _print_graceful_exit() -> None:
    print(f"{ANSI_GREEN}🍃 Graceful exit.{ANSI_RESET}", flush=True)


def main() -> int:
    options = parse_args(sys.argv[1:])
    app = QApplication(sys.argv)
    app.setApplicationName("Qt-Kurarin")

    window = PlayerWindow(frame_style=options.frame_style, verbose=options.verbose)
    exit_announced = False

    def graceful_exit() -> None:
        nonlocal exit_announced
        if exit_announced:
            return
        exit_announced = True
        window.shutdown()
        _print_graceful_exit()
        app.quit()

    def handle_sigint(signum, frame) -> None:
        del signum, frame
        QTimer.singleShot(0, graceful_exit)

    signal.signal(signal.SIGINT, handle_sigint)
    heartbeat = QTimer()
    heartbeat.start(100)
    heartbeat.timeout.connect(lambda: None)

    window.show()
    window.start()
    try:
        return app.exec()
    finally:
        heartbeat.stop()


if __name__ == "__main__":
    raise SystemExit(main())
