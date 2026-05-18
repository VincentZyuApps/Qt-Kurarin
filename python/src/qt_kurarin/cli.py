from __future__ import annotations

import argparse
from dataclasses import dataclass


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
        raise argparse.ArgumentTypeError("loudness must be an integer from 0 to 100") from exc
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
    verbose: bool = False
    textual_tui: bool = False
    tui_stdio: bool = False
    loudness: int = 100


def parse_args(argv: list[str] | None = None) -> AppOptions:
    parser = argparse.ArgumentParser(
        prog="qt-kurarin",
        description="Play the Qt-Kurarin desktop animation sequence.",
        formatter_class=CliHelpFormatter,
    )
    parser.add_argument(
        "--frame-style",
        choices=FRAME_STYLE_CHOICES,
        default=FRAME_STYLE_NONE,
        metavar="<style>",
        help="Window-like frame style for each animated sprite.",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print live sprite playback details to the console.",
    )
    output_group.add_argument(
        "-t",
        "--textual-tui",
        action="store_true",
        help="Show live playback details in a Textual TUI.",
    )
    parser.add_argument(
        "--tui-stdio",
        action="store_true",
        help=argparse.SUPPRESS,
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
        verbose=args.verbose,
        textual_tui=args.textual_tui,
        tui_stdio=args.tui_stdio,
        loudness=args.loudness,
    )
