```shell
cd Qt-Kurarin/python
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main
uv run python -m qt_kurarin.main --help
uv run qt-kurarin --frame-style win11 -l 30
uv run qt-kurarin --frame-style mac -l 30
uv run qt-kurarin --frame-style mac --tui-debug-stderr -l 30
uv run qt-kurarin --console-mode debug
uv run qt-kurarin --console-mode silent -l 30

## CI / CD:
cd Qt-Kurarin/python
# cd D:\aaaStuffsaaa\from_git\github\Qt-Kurarin\python
rm -r ./dist
# Remove-Item -Recurse -Force .\dist
uv build
uv run twine check .\dist\*
# 用环境变量 比如Powershell：
$env:UV_PUBLISH_TOKEN="pypi-YourTestPyPIToken"
uv publish --publish-url https://test.pypi.org/legacy/

$env:UV_PUBLISH_TOKEN="pypi-YourPyPIToken"
uv publish --publish-url https://upload.pypi.org/legacy/

uv run python -m compileall src
```