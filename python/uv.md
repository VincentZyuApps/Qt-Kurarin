## Dev & Test, run from source

```shell
cd Qt-Kurarin/python
uv venv --python 3.13
uv pip install -r ./requirements.txt
uv run python -m qt_kurarin.main
uv run python -m qt_kurarin.main --help
uv run qt-kurarin --help

cd Qt-Kurarin/python
# cd D:\aaaStuffsaaa\from_git\github\Qt-Kurarin\python
rm -r ./dist
# Remove-Item -Recurse -Force .\dist
uv build
uv run twine check .\dist\*
# use env, for example, in Powershell：
$env:UV_PUBLISH_TOKEN="pypi-YourTestPyPIToken"
uv publish --publish-url https://test.pypi.org/legacy/

$env:UV_PUBLISH_TOKEN="pypi-YourPyPIToken"
uv publish --publish-url https://upload.pypi.org/legacy/

uv run python -m compileall src
```

## Test & Prod, run from pypi
```shell
$Env:HTTP_PROXY = "http://127.0.0.1:7890"
$Env:HTTPS_PROXY = "http://127.0.0.1:7890"
Invoke-WebRequest -Uri "https://www.google.com" -Method Head -UseBasicParsing

# test different python version:

rm -r ./.venv/
uv venv --python 3.10
uv pip install qt-kurarin==0.2.4b2 --index-url https://pypi.org/simple
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --console-mode tui --loudness 50

rm -r ./.venv/
uv venv --python 3.11
uv pip install qt-kurarin==0.2.4b2 --index-url https://pypi.org/simple
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --console-mode tui --loudness 50

rm -r ./.venv/
uv venv --python 3.12
uv pip install qt-kurarin==0.2.4b2 --index-url https://pypi.org/simple
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --console-mode tui --loudness 50

rm -r ./.venv/
uv venv --python 3.13
uv pip install qt-kurarin==0.2.4b2 --index-url https://pypi.org/simple
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --console-mode tui --loudness 50

rm -r ./.venv/
uv venv --python 3.14
uv pip install qt-kurarin==0.2.4b2 --index-url https://pypi.org/simple
uv run qt-kurarin --help
uv run qt-kurarin --frame-style win11 --console-mode tui --loudness 50

```