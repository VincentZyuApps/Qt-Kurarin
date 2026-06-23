![Qt-Kurarin](https://socialify.git.ci/VincentZyuApps/Qt-Kurarin/image?custom_description=Qt-powered+Kyuukurarin+%28%E3%81%8D%E3%82%85%E3%81%86%E3%81%8F%E3%82%89%E3%82%8A%E3%82%93%29+on+your+desktop+%E2%80%94+animated+sprites+in+sync+with+the+music+&description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F0b%2FQt_logo_2016.svg%2F960px-Qt_logo_2016.svg.png&name=1&owner=1&pulls=1&stargazers=1&theme=Auto)

# 🎬 Qt-Kurarin Python プロトタイプ

> 🖥️ Qt-powered Kyuukurarin (きゅうくらりん) on your desktop — animated sprites in sync with the music 🎵

> **[📖 English](README.md)**
> **[📖 简体中文(大陆)](README.zh-cn.md)**
> **[📖 日本語](README.jp.md)**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/Qt-Kurarin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/qt-kurarin)

[![Package Version](https://img.shields.io/pypi/v/qt-kurarin?style=for-the-badge&logo=pypi&logoColor=white&label=Package%20Version&color=3775A9)](https://pypi.org/project/qt-kurarin/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/qt-kurarin?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI%20Downloads&color=FFD242)](https://pypi.org/project/qt-kurarin/)
[![Supported Versions](https://img.shields.io/pypi/pyversions/qt-kurarin?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/qt-kurarin/)

[![socket.dev](https://img.shields.io/badge/socket.dev-A855F7?style=for-the-badge&logo=socketdotdev&logoColor=white)](https://socket.dev/pypi/package/qt-kurarin)

これは PyQt6 ベースの再実装ラインであり、[元プロジェクト](https://github.com/VincentZyu233/Win-kurarin)の中核演出をデスクトップ上で検証するためのものです：

- 複数の独立したトップレベルウィンドウ
- 透過背景
- タイムライン駆動の移動アニメーション
- フェードイン / フェードアウト
- 常時最前面表示

| プラットフォーム | プレビュー |
|:---|:---:|
| Windows 11 | ![Windows 11](docs/images/preview.windows11.png) |
| Debian 13 + KDE Wayland | ![Debian 13 + KDE](docs/images/preview.debian13.kde.wayland.png) |
| Ubuntu 24.04 + LXQt X11 | ![Ubuntu 24.04 + LXQt](docs/images/preview.ubuntu24.lxqt.x11.png) |
| macOS 14 Sonoma | ![macOS 14](docs/images/preview.macos14.png) |

現在のビルドで読み込むもの：

- `data/script.txt`
- `resources/audio.mp3`
- `resources/*.png`

## 📥 ソースから実行

```shell
git clone https://github.com/VincentZyuApps/Qt-Kurarin
# または Gitee からクローン（中国本土で高速）：
git clone https://gitee.com/vincent-zyu/qt-kurarin
cd Qt-Kurarin/python
# uv is recommended
# https://docs.astral.sh/uv/getting-started/installation/
# https://gitee.com/wangnov/uv-custom/releases
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main [オプション]
```

## 📦 PyPI から実行

```shell
rm -r ./.venv/ # すでに存在する場合
uv venv --python 3.13
uv pip install qt-kurarin
# uv pip install qt-kurarin --index-url https://pypi.org/simple  # ミラーが更新されていない場合は公式ソースを試す
uv run qt-kurarin [オプション]
# qt-kurarin は通常の Python パッケージでもあります。以下の方法でも実行できます：
uv run python -m qt_kurarin.main [オプション]
```

## ⚙️ オプション

| フラグ | 説明 | デフォルト |
|--------|------|-----------|
| `-s, --frame-style <STYLE>` | ウィンドウ枠スタイル：`none`、`win11`、`mac` | `none` |
| `-c, --console-mode <MODE>` | 出力モード：`tui`*（Textual TUI）*、`debug`*（詳細コンソール）*、`silent`*（出力なし）* | `tui` |
| `-n, --hide-taskbar-button` | タスクバー/ドックアイコンを非表示*（Win: ✅ 確実、macOS: 🟡 非表示かも、Linux: ❓ コンポジター次第）* | オフ |
| `-f, --fps <rate>` | アニメーションループの目標フレームレート | `60` |
| `-l`, `--loudness <0-100>` | オーディオ音量パーセント | `100` |

## 💡 使用例

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

## 🖼️ 壁紙

> 💡 壁紙を自分で生成：[`docs/images/wallpaper/gen_wallpaper.py`](docs/images/wallpaper/gen_wallpaper.py)
> 💡 壁紙画像をクリックしてフル解像度で表示、右クリックで保存。
> 🎨 壁紙サイズ：1600×900 px — ベースカラー：`#FFD0D8`（ソフトピンク）

[![wallpaper](docs/images/wallpaper/wallpaper_1600x900_FFD0D8.png)](docs/images/wallpaper/wallpaper_1600x900_FFD0D8.png)

## 🙏 謝辞

> 🎵 **[原曲・MV](https://www.youtube.com/watch?v=2b1IexhKPz4)** — Iyowa  
> 💻 **[元 C# プログラム](https://www.nicovideo.jp/watch/sm41820938)** — Misaki  
> 🐍 **[PyQt 移植版](https://github.com/VincentZyuApps/Qt-Kurarin)** — VincentZyu

| | X | YouTube | niconico | Bilibili |
|---|---|---|---|---|
| 🎵 Iyowa | [![Post](https://img.shields.io/badge/Post-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/igusuri_please/status/1564026167241637888) | [![Video](https://img.shields.io/badge/Video-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=2b1IexhKPz4) | [![Video](https://img.shields.io/badge/Video-231815?style=flat-square&logo=niconico&logoColor=white)](https://www.nicovideo.jp/watch/sm39257413) | [![Video](https://img.shields.io/badge/Video-00A1D6?style=flat-square&logo=bilibili&logoColor=white)](https://www.bilibili.com/video/BV1MQ4y1a7JY) |
| 💻 Misaki | [![Post](https://img.shields.io/badge/Post-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/0x7FF/status/1619550154599829505) | [![Video](https://img.shields.io/badge/Video-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=7v4Lo-4Imp8) | [![Video](https://img.shields.io/badge/Video-231815?style=flat-square&logo=niconico&logoColor=white)](https://www.nicovideo.jp/watch/sm41820938) | [![Video](https://img.shields.io/badge/Video-00A1D6?style=flat-square&logo=bilibili&logoColor=white)](https://www.bilibili.com/video/BV1pK4ZzUENm) |
| 🐍 VincentZyu | [![Post](https://img.shields.io/badge/Post-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/VincentZyu233/status/2057339727762911467) | [![Video](https://img.shields.io/badge/Video-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://youtu.be/CTas1u2NFhQ?si=X3Vq50d5LIQhYyiV) | — | [![Video](https://img.shields.io/badge/Video-00A1D6?style=flat-square&logo=bilibili&logoColor=white)](https://www.bilibili.com/video/BV1DcLx6aEuh) |

## 📝 プラットフォーム補足

### 🪟 `--hide-taskbar-button`

各プラットフォームにおける動作の技術的解説：

**Windows** ✅ 確実。`Tool` ウィンドウフラグを設定し、Win32 API の `WS_EX_TOOLWINDOW` 拡張スタイルに相当します。タスクバーや Alt+Tab 一覧には表示されませんが、最前面表示は維持されます。

**macOS** 🟡 おそらく非表示、保証なし。`WindowStaysOnTopHint` と組み合わせるとフローティングツールパネルとして扱われ、通常は Dock アイコンが表示されません。ただし一部の macOS バージョンでは Dock に表示される場合があります。

**Linux/Wayland** ❌ ほぼ無効。Wayland コンポジターがタスクバーの動作を独立して制御するためです — KWin (KDE) は `Tool` フラグを完全に無視し、GNOME/Mutter は部分的に無視し、wlroots 系（Hyprland、Sway）も通常は無視します。

**Linux/X11** 🟡 ウィンドウマネージャー次第。KWin は `Tool` フラグを尊重しタスクバーエントリを非表示にします。GNOME/Mutter は部分的に尊重します。タイル型 WM（i3、bspwm）には従来のタスクバー概念がないため、フラグに可視効果はありません。

> 📝 本情報は経験およびオンライン調査に基づきます。実際の動作は OS バージョン、デスクトップ環境、設定によって異なる場合があります。
