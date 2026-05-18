"""Convert logo.ico → logo.png using Pillow (handles multi-frame .ico correctly)."""

from pathlib import Path
from PIL import Image

ico_path = Path(__file__).parent / "logo.ico"
png_path = Path(__file__).parent / "logo.png"

img = Image.open(ico_path)
# Pick the largest frame (typically 256x256 for modern .ico files)
sizes = img.info.get("sizes") or []
if sizes:
    best = max(sizes, key=lambda s: s[0] * s[1])
    img.size = best

img.save(png_path, "PNG")
print(f"Converted {ico_path.name} -> {png_path.name} ({img.size[0]}x{img.size[1]})")
