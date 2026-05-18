```shell
cd Qt-Kurarin/python
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main
uv run python -m qt_kurarin.main --help
uv run qt-kurarin --frame-style win11 --textual-tui -l 30
uv run qt-kurarin --frame-style mac --textual-tui -l 30
uv run qt-kurarin --frame-style mac --textual-tui --tui-debug-stderr -l 30

## cicd:
cd Qt-Kurarin/python
# cd D:\aaaStuffsaaa\from_git\github\Qt-Kurarin\python
Remove-Item -Recurse -Force .\dist
uv build
uv run twine check .\dist\*
# 用环境变量 比如Powershell：
$env:UV_PUBLISH_TOKEN="pypi-你的TestPyPI令牌"
uv publish --publish-url https://test.pypi.org/legacy/

$env:UV_PUBLISH_TOKEN="pypi-你的正式PyPI令牌"
uv publish --publish-url https://upload.pypi.org/legacy/

uv run python -m compileall src
```