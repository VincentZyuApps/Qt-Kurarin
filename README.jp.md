![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# Qt-Kurarin Python プロトタイプ

> Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/Qt-Kurarin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/qt-kurarin)

[![PyPI](https://img.shields.io/badge/PyPI-3776AB?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/qt-kurarin/)

これは PyQt6 ベースの再実装ラインであり、[元プロジェクト](https://github.com/VincentZyu233/Win-kurarin)の中核演出をデスクトップ上で検証するためのものです：

- 複数の独立したトップレベルウィンドウ
- 透過背景
- タイムライン駆動の移動アニメーション
- フェードイン / フェードアウト
- 常時最前面表示

現在のビルドで読み込むもの：

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

## ソースから実行

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
# or from gitee
git clone https://gitee.com/vincent-zyu/qt-kurarin
cd Qt-Kurarin/python
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main
uv run python -m qt_kurarin.main --frame-style none
uv run python -m qt_kurarin.main --frame-style win11
uv run python -m qt_kurarin.main --frame-style mac
uv run qt-kurarin --frame-style none --verbose
uv run qt-kurarin --frame-style win11 --verbose
uv run qt-kurarin --frame-style mac --verbose
```

## PyPI から実行
```shell
rm -r ./.venv/ # すでに存在する場合
uv venv --python 3.13
uv pip install qt-kurarin
# uv pip install qt-kurarin --index-url https://pypi.org/simple  # ミラーが更新されていない場合は公式ソースを試す
uv run qt-kurarin
uv run qt-kurarin --frame-style none
uv run qt-kurarin --frame-style win11
uv run qt-kurarin --frame-style mac
uv run qt-kurarin --frame-style none --verbose
uv run qt-kurarin --frame-style win11 --verbose
uv run qt-kurarin --frame-style mac --verbose
```
