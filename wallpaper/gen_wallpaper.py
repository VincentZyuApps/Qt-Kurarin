#!/usr/bin/env python3
"""
Generate a 1600x900 solid-color wallpaper (#FFD0D8)
to match the Win-kurarin project theme.

Usage:
    python gen_wallpaper.py
    python gen_wallpaper.py --color FFD0D8 --width 1920 --height 1080
"""

import argparse
import struct
import zlib
from pathlib import Path


def create_png(width: int, height: int, color_hex: str) -> bytes:
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)

    raw_data = b""
    for _ in range(height):
        raw_data += b"\x00"  # filter byte
        raw_data += struct.pack("BBB", r, g, b) * width

    def chunk(chunk_type, data):
        c = chunk_type + data
        return (
            struct.pack(">I", len(data))
            + c
            + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        )

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(raw_data))
    iend = chunk(b"IEND", b"")

    return header + ihdr + idat + iend


def main():
    parser = argparse.ArgumentParser(description="Generate a solid-color wallpaper")
    parser.add_argument("--color", default="FFD0D8", help="Hex color (default: FFD0D8)")
    parser.add_argument(
        "--width", type=int, default=1600, help="Image width (default: 1600)"
    )
    parser.add_argument(
        "--height", type=int, default=900, help="Image height (default: 900)"
    )
    args = parser.parse_args()

    color = args.color.lstrip("#")
    if len(color) != 6:
        print("❌ Color must be a 6-digit hex (e.g. FFD0D8)")
        return

    out_path = (
        Path(__file__).parent / f"wallpaper_{args.width}x{args.height}_{color}.png"
    )
    png_data = create_png(args.width, args.height, color)
    out_path.write_bytes(png_data)

    print(f"✅ Saved: {out_path}  ({len(png_data) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
