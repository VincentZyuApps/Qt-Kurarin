from __future__ import annotations

import argparse
from dataclasses import dataclass


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


def parse_args(argv: list[str] | None = None) -> AppOptions:
    parser = argparse.ArgumentParser(
        prog="qt-kurarin",
        description="Play the Qt-Kurarin desktop animation sequence.",
    )
    parser.add_argument(
        "--frame-style",
        choices=FRAME_STYLE_CHOICES,
        default=FRAME_STYLE_NONE,
        help="Window-like frame style for each animated sprite.",
    )
    args = parser.parse_args(argv)
    return AppOptions(frame_style=args.frame_style)
