![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# Qt-Kurarin Python 原型

> Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

这是一个基于 PyQt6 的重构路线，用来验证原项目核心效果在桌面上的复现方式：

- 多个彼此独立的顶层窗口
- 透明背景
- 基于时间轴的移动动画
- 淡入 / 淡出
- 始终置顶显示

当前构建会读取：

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

## 从源码运行

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
cd Qt-Kurarin/python
uv venv --python 3.12
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main
```

## 从 PyPI 运行
```shell
rm -r ./.venv/ # 如果已经存在
uv venv --python 3.12
uv pip install qt-kurarin
uv run qt-kurarin
```
