from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib.metadata import version as _pkg_version, PackageNotFoundError


class CliHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog: str) -> None:
        super().__init__(prog, max_help_position=34, width=100)

    def _format_action(self, action: argparse.Action) -> str:
        if not action.help:
            return super()._format_action(action)

        header = self._format_action_invocation(action)
        help_text = self._expand_help(action)
        lines = [f"  {header}\n"]
        for line in self._split_lines(help_text, self._width - 6):
            lines.append(f"      {line}\n")
        return "".join(lines)


def _loudness_value(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "loudness must be an integer from 0 to 100"
        ) from exc
    if not 0 <= parsed <= 100:
        raise argparse.ArgumentTypeError("loudness must be an integer from 0 to 100")
    return parsed


FRAME_STYLE_NONE = "none"
FRAME_STYLE_WIN11 = "win11"
FRAME_STYLE_MAC = "mac"
FRAME_STYLE_CHOICES = (
    FRAME_STYLE_NONE,
    FRAME_STYLE_WIN11,
    FRAME_STYLE_MAC,
)


@dataclass(slots=True)
class AppOptions:
    frame_style: str = FRAME_STYLE_NONE
    console_mode: str = "tui"
    tui_port: int | None = None
    tui_debug_stderr: bool = False
    hide_taskbar: bool = False
    fps: int = 60
    loudness: int = 100


try:
    __version__ = _pkg_version("qt-kurarin")
except PackageNotFoundError:
    __version__ = "0.0.0"


def parse_args(argv: list[str] | None = None) -> AppOptions:
    parser = argparse.ArgumentParser(
        prog="qt-kurarin",
        description="Play the Qt-Kurarin desktop animation sequence.",
        formatter_class=CliHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"qt-kurarin {__version__}",
    )
    parser.add_argument(
        "-s",
        "--frame-style",
        choices=FRAME_STYLE_CHOICES,
        default=FRAME_STYLE_NONE,
        metavar="<style>",
        help="Window-like frame style for each animated sprite.",
    )
    parser.add_argument(
        "-c",
        "--console-mode",
        choices=("tui", "debug", "silent"),
        default="tui",
        metavar="<mode>",
        help="Console output mode: tui (Textual TUI), debug (verbose console), silent (no output).",
    )
    parser.add_argument("--tui-port", type=int, help=argparse.SUPPRESS)
    parser.add_argument(
        "--tui-debug-stderr", action="store_true", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-n",
        "--hide-taskbar-button",
        action="store_true",
        help="Hide the taskbar/dock icon for the animated window. "
        "Tested on Windows 10/11 (works reliably). "
        "macOS may hide the Dock icon; "
        "Linux depends on the compositor (KWin likely works, "
        "GNOME/Wayland likely does not). "
        "Not guaranteed across all platforms.",
    )
    parser.add_argument(
        "-f",
        "--fps",
        type=int,
        default=60,
        metavar="<rate>",
        help="Target frame rate for the animation loop (default: 60).",
    )
    parser.add_argument(
        "-l",
        "--loudness",
        type=_loudness_value,
        default=100,
        metavar="<percent>",
        help="Audio loudness percentage from 0 to 100.",
    )
    args = parser.parse_args(argv)
    return AppOptions(
        frame_style=args.frame_style,
        console_mode=args.console_mode,
        tui_port=args.tui_port,
        tui_debug_stderr=args.tui_debug_stderr,
        hide_taskbar=args.hide_taskbar_button,
        fps=args.fps,
        loudness=args.loudness,
    )
