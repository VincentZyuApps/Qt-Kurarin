from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parent
ICO_PATH = ROOT / "logo.ico"
PNG_PATH = ROOT / "logo.png"
MAC_PNG_PATH = ROOT / "logo_macos_512.png"
ICNS_PATH = ROOT / "logo.icns"
ICONSET_DIR = ROOT / "logo.iconset"


def load_source_image() -> Image.Image:
    if PNG_PATH.exists():
        return Image.open(PNG_PATH).convert("RGBA")
    if ICO_PATH.exists():
        image = Image.open(ICO_PATH)
        sizes = image.info.get("sizes") or []
        if sizes:
            best = max(sizes, key=lambda size: size[0] * size[1])
            image.size = best
        return image.convert("RGBA")
    raise FileNotFoundError("Neither logo.png nor logo.ico exists.")


def write_macos_png(image: Image.Image) -> None:
    resized = image.resize((512, 512), Image.Resampling.LANCZOS)
    resized.save(MAC_PNG_PATH, "PNG")
    print(f"Wrote {MAC_PNG_PATH.name} (512x512)")


def write_iconset(image: Image.Image) -> None:
    if ICONSET_DIR.exists():
        shutil.rmtree(ICONSET_DIR)
    ICONSET_DIR.mkdir(parents=True, exist_ok=True)
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]
    for size, name in sizes:
        image.resize((size, size), Image.Resampling.LANCZOS).save(ICONSET_DIR / name, "PNG")


def write_icns() -> None:
    iconutil = shutil.which("iconutil")
    if iconutil is None:
        print("iconutil not found; skipped logo.icns generation.")
        return
    subprocess.run(
        [iconutil, "-c", "icns", str(ICONSET_DIR), "-o", str(ICNS_PATH)],
        check=True,
    )
    print(f"Wrote {ICNS_PATH.name}")


def main() -> None:
    image = load_source_image()
    write_macos_png(image)
    write_iconset(image)
    write_icns()


if __name__ == "__main__":
    main()
