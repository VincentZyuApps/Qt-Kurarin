from __future__ import annotations

from pathlib import Path
import socket
import signal
import subprocess
import sys
from threading import Lock, Thread

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from .cli import parse_args
from .tui import run_socket_tui, snapshot_to_json
from .window import PlayerWindow, resolve_app_icon_path


ANSI_GREEN = "\033[92m"
ANSI_RESET = "\033[0m"


def _print_graceful_exit() -> None:
    print(f"{ANSI_GREEN}🍃 Graceful exit.{ANSI_RESET}", flush=True)


def main() -> int:
    options = parse_args(sys.argv[1:])

    if options.tui_port is not None:
        return run_socket_tui(options.tui_port)

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
        fps=options.fps,
    )
    exit_announced = False
    tui_process: subprocess.Popen[str] | None = None
    tui_timer: QTimer | None = None
    tui_exit_reported = False
    tui_server: socket.socket | None = None
    tui_connection: socket.socket | None = None
    tui_connection_lock = Lock()

    def debug_tui(message: str) -> None:
        if options.tui_debug_stderr:
            print(f"[tui debug] {message}", flush=True)

    def graceful_exit() -> None:
        nonlocal exit_announced
        if exit_announced:
            return
        exit_announced = True
        if tui_timer is not None and tui_timer.isActive():
            tui_timer.stop()
        with tui_connection_lock:
            if tui_connection is not None:
                try:
                    tui_connection.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    tui_connection.close()
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
        tui_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tui_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tui_server.bind(("127.0.0.1", 0))
        tui_server.listen(1)
        tui_port = tui_server.getsockname()[1]
        debug_tui(f"listening on 127.0.0.1:{tui_port}")

        def accept_tui_connection() -> None:
            nonlocal tui_connection
            assert tui_server is not None
            try:
                connection, _ = tui_server.accept()
            except OSError:
                debug_tui("accept() aborted before TUI connected")
                return
            with tui_connection_lock:
                tui_connection = connection
            debug_tui("TUI subprocess connected to snapshot socket")

        tui_process = subprocess.Popen(
            [sys.executable, "-m", "qt_kurarin.main", "--tui-port", str(tui_port)],
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        debug_tui(f"spawned TUI subprocess pid={tui_process.pid}")
        Thread(target=accept_tui_connection, daemon=True).start()
        tui_timer = QTimer()
        tui_timer.setInterval(120)

        def push_snapshot() -> None:
            nonlocal tui_exit_reported
            if tui_process is None:
                return
            if tui_process.poll() is not None:
                if not tui_exit_reported:
                    tui_exit_reported = True
                    print(
                        f"[warning] Textual TUI exited (code {tui_process.poll()}). GUI continuing.",
                        flush=True,
                    )
                    debug_tui("TUI subprocess exited before next snapshot push")
                tui_timer.stop()
                return
            with tui_connection_lock:
                connection = tui_connection
            if connection is None:
                return
            try:
                connection.sendall(
                    (snapshot_to_json(window.get_snapshot()) + "\n").encode("utf-8")
                )
            except OSError:
                if not tui_exit_reported:
                    tui_exit_reported = True
                    print(
                        "[warning] Lost connection to Textual TUI. GUI continuing.",
                        flush=True,
                    )
                    debug_tui("snapshot socket send failed")
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
        with tui_connection_lock:
            if tui_connection is not None:
                try:
                    tui_connection.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    tui_connection.close()
                except OSError:
                    pass
        if tui_server is not None:
            try:
                tui_server.close()
            except OSError:
                pass
        if tui_process is not None:
            try:
                tui_process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                tui_process.terminate()


if __name__ == "__main__":
    raise SystemExit(main())
