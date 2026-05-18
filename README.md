![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Light)

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
