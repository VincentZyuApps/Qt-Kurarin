![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# Qt-Kurarin Python 原型

> Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/Qt-Kurarin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/qt-kurarin)

[![PyPI](https://img.shields.io/badge/PyPI-3776AB?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/qt-kurarin/)
[![PyPI version](https://img.shields.io/pypi/v/qt-kurarin?style=for-the-badge&logo=pypi&logoColor=white&label=Version&color=3775A9)](https://pypi.org/project/qt-kurarin/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qt-kurarin?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=FFD242)](https://pypi.org/project/qt-kurarin/)

这是一个基于 PyQt6 的重构路线，用来验证[原项目](https://github.com/VincentZyu233/Win-kurarin)核心效果在桌面上的复现方式：

- 多个彼此独立的顶层窗口
- 透明背景
- 基于时间轴的移动动画
- 淡入 / 淡出
- 始终置顶显示

| 平台 | 预览 |
|:---|:---:|
| Windows 11 | ![Windows 11](docs/images/preview.windows11.png) |
| Debian 13 + KDE Wayland | ![Debian 13 + KDE](docs/images/preview.debian13.kde.wayland.png) |
| macOS 14 Sonoma | ![macOS 14](docs/images/preview.macos14.png) |

当前构建会读取：

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

## 从源码运行

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
# 或从 Gitee 克隆（国内访问更快）：
git clone https://gitee.com/vincent-zyu/qt-kurarin
cd Qt-Kurarin/python
# uv is recommended
# https://docs.astral.sh/uv/getting-started/installation/
# https://gitee.com/wangnov/uv-custom/releases
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main [选项]
```

## 从 PyPI 运行

```shell
rm -r ./.venv/ # 如果已经存在
uv venv --python 3.13
uv pip install qt-kurarin
# uv pip install qt-kurarin --index-url https://pypi.org/simple  # 镜像源没刷新可试试官方源
uv run qt-kurarin [选项]
```

## 选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-f, --frame-style <STYLE>` | 窗口边框样式：`none`、`win11`、`mac` | `none` |
| `-v`, `--verbose` | 在控制台实时输出精灵播放调试信息 | 关闭 |
| `-t`, `--textual-tui` | 在 Textual TUI 中实时显示播放详情 | 关闭 |
| `-n, --hide-taskbar-button` | 隐藏任务栏/程序坞图标（Win: ✅ 可靠，macOS: 🟡 可能隐藏，Linux: ❓ 取决于合成器） | 关闭 |
| `--fps <rate>` | 动画循环的目标帧率 | `60` |
| `-l`, `--loudness <0-100>` | 音频音量百分比 | `100` |

## 示例

```shell
uv run qt-kurarin
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --textual-tui
uv run qt-kurarin --frame-style mac --verbose
uv run qt-kurarin --loudness 60
```

## 壁纸

> 💡 可以自行生成壁纸：[`wallpaper/gen_wallpaper.py`](wallpaper/gen_wallpaper.py)
> 💡 点击壁纸图片可查看原分辨率，右键另存为即可保存。
> 🎨 壁纸尺寸：1600×900 px — 基础色：`#FFD0D8`（柔粉色）

[![wallpaper](wallpaper/wallpaper_1600x900_FFD0D8.png)](wallpaper/wallpaper_1600x900_FFD0D8.png)

## 平台说明

### `--hide-taskbar-button`

该参数在各平台行为的技术详解：

**Windows** ✅ 可靠。设置 `Tool` 窗口标志，对应 Win32 API 的 `WS_EX_TOOLWINDOW` 扩展样式。窗口不会出现在任务栏或 Alt+Tab 列表中，但仍保持置顶显示。

**macOS** 🟡 大概率生效，不保证。与 `WindowStaysOnTopHint` 结合使用时，macOS 将其视为浮动工具面板，通常没有 Dock 图标。但在部分 macOS 版本上，单一 Tool 窗口可能仍会显示在 Dock 中。

**Linux/Wayland** ❌ 几乎不生效。Wayland 协议下，合成器独立控制任务栏行为 — KWin (KDE) 完全忽略 `Tool` 标志，GNOME/Mutter 部分忽略，wlroots 系合成器（Hyprland、Sway）通常也忽略。

**Linux/X11** 🟡 取决于窗口管理器。KWin 尊重 `Tool` 标志并隐藏任务栏条目；GNOME/Mutter 部分尊重；平铺 WM（i3、bspwm）没有传统任务栏概念，标志无可见效果。

> 📝 以上信息基于经验及互联网搜索资料得出，仅供参考。实际行为可能因操作系统版本、桌面环境及配置不同而有所差异。
