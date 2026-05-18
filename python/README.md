# Qt-Kurarin Python Prototype

This is a PyQt6 reconstruction track for validating the core effect of the original project:

- multiple independent top-level windows
- transparent backgrounds
- timeline-driven movement
- fade in / fade out
- always-on-top presentation

The current build reads:

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

## Migrate assets from Win-kurarin

From the repository root:

```powershell
python .\scripts\migrate_win_kurarin.py D:\aaaStuffsaaa\from_git\github\Win-kurarin
```

The script will:

- extract `String1` from `KyukurarinForm\asset.resx`
- write it to `python\data\script.txt`
- copy all `.png` and `.mp3` files from `KyukurarinForm\Resources\` into `python\resources\`

## Run

```powershell
cd Qt-Kurarin/python
uv venv --python 3.12
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main
```
