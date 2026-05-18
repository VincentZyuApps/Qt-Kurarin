from __future__ import annotations

from pathlib import Path
import signal
import subprocess
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from .cli import parse_args
from .tui import run_stdio_tui, snapshot_to_json
from .window import PlayerWindow, resolve_app_icon_path


ANSI_GREEN = "\033[92m"
ANSI_RESET = "\033[0m"


def _print_graceful_exit() -> None:
    print(f"{ANSI_GREEN}🍃 Graceful exit.{ANSI_RESET}", flush=True)


def main() -> int:
    options = parse_args(sys.argv[1:])

    if options.tui_stdio:
        return run_stdio_tui()

    app = QApplication(sys.argv)
    app.setApplicationName("Qt-Kurarin")
    package_dir = Path(__file__).resolve().parent
    icon_path = resolve_app_icon_path(package_dir)
    if icon_path is not None:
        app.setWindowIcon(QIcon(str(icon_path)))

    window = PlayerWindow(
        frame_style=options.frame_style,
        verbose=options.verbose,
        loudness=options.loudness,
        hide_taskbar=options.hide_taskbar,
    )
    exit_announced = False
    tui_process: subprocess.Popen[str] | None = None
    tui_timer: QTimer | None = None

    def graceful_exit() -> None:
        nonlocal exit_announced
        if exit_announced:
            return
        exit_announced = True
        if tui_timer is not None and tui_timer.isActive():
            tui_timer.stop()
        if (
            tui_process is not None
            and tui_process.stdin is not None
            and not tui_process.stdin.closed
        ):
            try:
                tui_process.stdin.close()
            except OSError:
                pass
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

    if options.textual_tui:
        tui_process = subprocess.Popen(
            [sys.executable, "-m", "qt_kurarin.main", "--tui-stdio"],
            stdin=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        tui_timer = QTimer()
        tui_timer.setInterval(120)

        def push_snapshot() -> None:
            if tui_process is None or tui_process.stdin is None:
                return
            if tui_process.poll() is not None:
                tui_timer.stop()
                return
            try:
                tui_process.stdin.write(snapshot_to_json(window.get_snapshot()) + "\n")
                tui_process.stdin.flush()
            except OSError:
                tui_timer.stop()

        tui_timer.timeout.connect(push_snapshot)
        tui_timer.start()
        push_snapshot()

    window.show()
    window.start()
    try:
        return app.exec()
    finally:
        heartbeat.stop()
        if tui_timer is not None and tui_timer.isActive():
            tui_timer.stop()
        if tui_process is not None:
            if tui_process.stdin is not None and not tui_process.stdin.closed:
                try:
                    tui_process.stdin.close()
                except OSError:
                    pass
            try:
                tui_process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                tui_process.terminate()


if __name__ == "__main__":
    raise SystemExit(main())
