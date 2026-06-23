![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# 🎬 Qt-Kurarin Python Prototype

> 🖥️ Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music 🎵

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/Qt-Kurarin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/qt-kurarin)

[![PyPI](https://img.shields.io/badge/PyPI-3776AB?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/qt-kurarin/)
[![PyPI version](https://img.shields.io/pypi/v/qt-kurarin?style=for-the-badge&logo=pypi&logoColor=white&label=Version&color=3775A9)](https://pypi.org/project/qt-kurarin/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qt-kurarin?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=FFD242)](https://pypi.org/project/qt-kurarin/)
[![Python Versions](https://img.shields.io/pypi/pyversions/qt-kurarin?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/qt-kurarin/)

This is a PyQt6 reconstruction track for validating the core effect of the [original project](https://github.com/VincentZyu233/Win-kurarin):

- multiple independent top-level windows
- transparent backgrounds
- timeline-driven movement
- fade in / fade out
- always-on-top presentation

| Platform | Preview |
|:---|:---:|
| Windows 11 | ![Windows 11](docs/images/preview.windows11.png) |
| Debian 13 + KDE Wayland | ![Debian 13 + KDE](docs/images/preview.debian13.kde.wayland.png) |
| Ubuntu 24.04 + LXQt X11 | ![Ubuntu 24.04 + LXQt](docs/images/preview.ubuntu24.lxqt.x11.png) |
| macOS 14 Sonoma | ![macOS 14](docs/images/preview.macos14.png) |

The current build reads:

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

## 📥 Run from source

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
# or from gitee: 
git clone https://gitee.com/vincent-zyu/qt-kurarin
cd Qt-Kurarin/python
# uv is recommended
# https://docs.astral.sh/uv/getting-started/installation/
# https://gitee.com/wangnov/uv-custom/releases
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main [OPTIONS]
```

## 📦 Run from PyPI

```shell
rm -r ./.venv/ # if already exist
uv venv --python 3.13
uv pip install qt-kurarin
# uv pip install qt-kurarin --index-url https://pypi.org/simple  # use official index if mirrors are not latest
uv run qt-kurarin [OPTIONS]
# qt-kurarin is also a regular Python package; run it with:
uv run python -m qt_kurarin.main [OPTIONS]
```

## ⚙️ Options

| Flag | Description | Default |
|------|-------------|---------|
| `-s, --frame-style <STYLE>` | Window frame style: `none`, `win11`, `mac` | `none` |
| `-c, --console-mode <MODE>` | Console output mode: `tui` *(Textual TUI)*, `debug` *(verbose console)*, `silent` *(no output)* | `tui` |
| `-n, --hide-taskbar-button` | Hide the taskbar/dock icon *(Win: ✅, macOS: 🟡 may hide, Linux: ❓ depends on compositor)* | off |
| `-f, --fps <rate>` | Target frame rate for the animation loop | `60` |
| `-l`, `--loudness <0-100>` | Audio loudness percentage | `100` |

## 💡 Examples

```shell
uv run qt-kurarin
uv run qt-kurarin --help
uv run qt-kurarin --fps 30
uv run qt-kurarin --loudness 60
uv run qt-kurarin --frame-style mac
uv run qt-kurarin --console-mode silent
uv run qt-kurarin --hide-taskbar-button
uv run qt-kurarin --frame-style mac --console-mode silent
uv run qt-kurarin --frame-style win11 --console-mode debug --loudness 20
uv run qt-kurarin --frame-style none --console-mode debug --loudness 80 --fps 30 --hide-taskbar-button
```

## 🖼️ Wallpaper

> 💡 Generate your own wallpaper: [`docs/images/wallpaper/gen_wallpaper.py`](docs/images/wallpaper/gen_wallpaper.py)
> 💡 Click the wallpaper image to view full resolution, then right-click to save.
> 🎨 Wallpaper size: 1600×900 px — base color: `#FFD0D8` (soft pink)

[![wallpaper](docs/images/wallpaper/wallpaper_1600x900_FFD0D8.png)](docs/images/wallpaper/wallpaper_1600x900_FFD0D8.png)

## 🙏 Acknowledgments

> 🎵 **[Original Music & MV](https://www.youtube.com/watch?v=2b1IexhKPz4)** — Iyowa  
> 💻 **[Original C# Program](https://www.nicovideo.jp/watch/sm41820938)** — Misaki  
> 🐍 **[PyQt Port](https://github.com/VincentZyuApps/Qt-Kurarin)** — VincentZyu

| | X | YouTube | niconico | Bilibili |
|---|---|---|---|---|
| 🎵 Iyowa | [![Post](https://img.shields.io/badge/Post-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/igusuri_please/status/1564026167241637888) | [![Video](https://img.shields.io/badge/Video-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=2b1IexhKPz4) | [![Video](https://img.shields.io/badge/Video-231815?style=flat-square&logo=niconico&logoColor=white)](https://www.nicovideo.jp/watch/sm39257413) | [![Video](https://img.shields.io/badge/Video-00A1D6?style=flat-square&logo=bilibili&logoColor=white)](https://www.bilibili.com/video/BV1MQ4y1a7JY) |
| 💻 Misaki | [![Post](https://img.shields.io/badge/Post-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/0x7FF/status/1619550154599829505) | [![Video](https://img.shields.io/badge/Video-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=7v4Lo-4Imp8) | [![Video](https://img.shields.io/badge/Video-231815?style=flat-square&logo=niconico&logoColor=white)](https://www.nicovideo.jp/watch/sm41820938) | [![Video](https://img.shields.io/badge/Video-00A1D6?style=flat-square&logo=bilibili&logoColor=white)](https://www.bilibili.com/video/BV1pK4ZzUENm) |
| 🐍 VincentZyu | [![Post](https://img.shields.io/badge/Post-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/VincentZyu233/status/2057339727762911467) | [![Video](https://img.shields.io/badge/Video-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/CTas1u2NFhQ?si=X3Vq50d5LIQhYyiV) | — | [![Video](https://img.shields.io/badge/Video-00A1D6?style=flat-square&logo=bilibili&logoColor=white)](https://www.bilibili.com/video/BV1DcLx6aEuh) |

## 📝 Platform Notes

### 🪟 `--hide-taskbar-button`

Technical breakdown of how this flag behaves across operating systems:

**Windows** ✅ Reliable. Sets the `Tool` window flag, which maps to the Win32 `WS_EX_TOOLWINDOW` extended style. The window will not appear in the taskbar or Alt+Tab list, but remains always-on-top.

**macOS** 🟡 Likely works, not guaranteed. When combined with `WindowStaysOnTopHint`, macOS treats the window as a floating utility panel, which typically lacks a Dock icon. However, on some macOS versions, a single Tool window may still appear in the Dock.

**Linux/Wayland** ❌ Unlikely to work. Wayland compositors control taskbar behavior independently — KWin (KDE) ignores the `Tool` flag entirely, GNOME/Mutter partially ignores it, and wlroots-based compositors (Hyprland, Sway) generally ignore it as well.

**Linux/X11** 🟡 Depends on the window manager. KWin respects the `Tool` flag and hides the taskbar entry. GNOME/Mutter partially respects it. Tiling WMs (i3, bspwm) have no traditional taskbar concept, so the flag has no visible effect.

> 📝 This information is based on experience and online research. Actual behavior may vary depending on your specific OS version, desktop environment, and configuration.
