![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# Qt-Kurarin Python 原型

> Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/Qt-Kurarin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/qt-kurarin)

[![PyPI](https://img.shields.io/badge/PyPI-3776AB?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/qt-kurarin/)

这是一个基于 PyQt6 的重构路线，用来验证[原项目](https://github.com/VincentZyu233/Win-kurarin)核心效果在桌面上的复现方式：

- 多个彼此独立的顶层窗口
- 透明背景
- 基于时间轴的移动动画
- 淡入 / 淡出
- 始终置顶显示

当前构建会读取：

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

> 💡 可以自行生成壁纸：`wallpaper/gen_wallpaper.py`

![wallpaper](wallpaper/wallpaper_1600x900_FFD0D8.png)

## 从源码运行

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
# 或从 Gitee 克隆（国内访问更快）：
git clone https://gitee.com/vincent-zyu/qt-kurarin
cd Qt-Kurarin/python
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
| `--frame-style <STYLE>` | 窗口边框样式：`none`、`win11`、`mac` | `none` |
| `-v`, `--verbose` | 在控制台实时输出精灵播放调试信息 | 关闭 |
| `-t`, `--textual-tui` | 在 Textual TUI 中实时显示播放详情 | 关闭 |
| `--hide-taskbar-button` | 隐藏任务栏/程序坞图标（Win: ✅ 可靠，macOS: 🟡 可能隐藏，Linux: ❓ 取决于合成器） | 关闭 |
| `-l`, `--loudness <0-100>` | 音频音量百分比 | `100` |

## 示例

```shell
uv run qt-kurarin
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --textual-tui
uv run qt-kurarin --frame-style mac --verbose
uv run qt-kurarin --loudness 60
```
