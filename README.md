![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# Qt-Kurarin Python Prototype

> Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/Qt-Kurarin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/qt-kurarin)

[![PyPI](https://img.shields.io/badge/PyPI-3776AB?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/qt-kurarin/)

This is a PyQt6 reconstruction track for validating the core effect of the [original project](https://github.com/VincentZyu233/Win-kurarin):

- multiple independent top-level windows
- transparent backgrounds
- timeline-driven movement
- fade in / fade out
- always-on-top presentation

The current build reads:

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

> 💡 Generate your own wallpaper: `wallpaper/gen_wallpaper.py`

![wallpaper](wallpaper/wallpaper_1600x900_FFD0D8.png)

## Run from source

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
# or from gitee: 
git clone https://gitee.com/vincent-zyu/qt-kurarin
cd Qt-Kurarin/python
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main [OPTIONS]
```

## Run from PyPI

```shell
rm -r ./.venv/ # if already exist
uv venv --python 3.13
uv pip install qt-kurarin
# uv pip install qt-kurarin --index-url https://pypi.org/simple  # use official index if mirrors are not latest
uv run qt-kurarin [OPTIONS]
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--frame-style <STYLE>` | Window frame style: `none`, `win11`, `mac` | `none` |
| `-v`, `--verbose` | Print live sprite playback details to the console | off |
| `-t`, `--textual-tui` | Show live playback details in a Textual TUI | off |
| `-l`, `--loudness <0-100>` | Audio loudness percentage | `100` |

## Examples

```shell
uv run qt-kurarin
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --textual-tui
uv run qt-kurarin --frame-style mac --verbose
uv run qt-kurarin --loudness 60
```
