"""
cd Qt-kurarin
python .\scripts\migrate_win_kurarin.py <absolute-path>
e.g:
 python .\scripts\migrate_win_kurarin.py D:\aaaStuffsaaa\from_git\github\Win-kurarin
"""

from __future__ import annotations

import argparse
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Migrate reusable data from a Win-kurarin checkout into the "
            "Qt-Kurarin Python prototype."
        )
    )
    parser.add_argument(
        "source_root",
        type=Path,
        help="Absolute path to the root of the original Win-kurarin repository.",
    )
    parser.add_argument(
        "--target-python-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "python",
        help="Target Qt-Kurarin python directory. Defaults to this repo's python/ folder.",
    )
    return parser.parse_args()


def require_absolute_dir(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_absolute():
        raise ValueError(f"{label} must be an absolute path.")
    if not resolved.exists():
        raise FileNotFoundError(f"{label} does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"{label} is not a directory: {resolved}")
    return resolved


def extract_script(asset_resx_path: Path) -> str:
    tree = ET.parse(asset_resx_path)
    root = tree.getroot()

    for data in root.findall("data"):
        if data.attrib.get("name") != "String1":
            continue
        value = data.find("value")
        if value is None or value.text is None:
            raise ValueError("String1 exists in asset.resx but does not contain text.")
        return value.text.replace("\r\n", "\n")

    raise KeyError("Could not find String1 in asset.resx.")


def copy_resources(source_dir: Path, target_dir: Path) -> tuple[int, int]:
    copied = 0
    total_bytes = 0

    target_dir.mkdir(parents=True, exist_ok=True)
    for source_file in sorted(source_dir.iterdir()):
        if not source_file.is_file():
            continue
        if source_file.suffix.lower() not in {".png", ".mp3"}:
            continue

        target_file = target_dir / source_file.name
        shutil.copy2(source_file, target_file)
        copied += 1
        total_bytes += source_file.stat().st_size

    return copied, total_bytes


def main() -> int:
    args = parse_args()

    source_root = require_absolute_dir(args.source_root, "source_root")
    target_python_dir = require_absolute_dir(args.target_python_dir, "target_python_dir")

    source_project_dir = source_root / "KyukurarinForm"
    if not source_project_dir.is_dir():
        raise FileNotFoundError(
            f"Expected C# project directory at: {source_project_dir}"
        )

    asset_resx_path = source_project_dir / "asset.resx"
    resources_dir = source_project_dir / "Resources"
    if not asset_resx_path.is_file():
        raise FileNotFoundError(f"Missing asset.resx: {asset_resx_path}")
    if not resources_dir.is_dir():
        raise FileNotFoundError(f"Missing Resources directory: {resources_dir}")

    script_text = extract_script(asset_resx_path)

    data_dir = target_python_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    script_path = data_dir / "script.txt"
    script_path.write_text(script_text, encoding="utf-8", newline="\n")

    target_resources_dir = target_python_dir / "resources"
    copied_count, total_bytes = copy_resources(resources_dir, target_resources_dir)

    line_count = script_text.count("\n") + 1 if script_text else 0
    print(f"Source root      : {source_root}")
    print(f"Target python dir: {target_python_dir}")
    print(f"Script written   : {script_path}")
    print(f"Script lines     : {line_count}")
    print(f"Resources copied : {copied_count}")
    print(f"Bytes copied     : {total_bytes}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"Migration failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
