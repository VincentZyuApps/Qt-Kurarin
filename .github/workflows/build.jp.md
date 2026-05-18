# ビルドと公開ワークフロー

> **[📖 English](build.md)**
> **[📖 简体中文(大陆)](build.zh-cn.md)**
> **[📖 日本語](build.jp.md)**

このリポジトリでは、`python/` 配下の Python パッケージに対して、小規模な commit message 駆動ワークフローを使用しています。

## キーワード

| commit message 内のキーワード | wheel/sdist をビルド | PyPI へ公開 |
|---|:---:|:---:|
| `build action` | ✅ | ❌ |
| `publish pypi` | ✅ | ✅ |
| `pypi publish` | ✅ | ✅ |

## 例

```bash
# ビルドのみ
git commit --allow-empty -m "ci: verify package build (build action)"

# ビルドして PyPI に公開
git commit --allow-empty -m "release: v0.0.1-beta.1 (publish pypi)"
```

## 注意事項

- Pull request では常にビルドジョブが実行されますが、公開は行われません。
- パッケージのバージョンは `python/pyproject.toml` から読み取られます。
- リポジトリの README はルートにあり、CI はビルド前にそれを `python/README.md` にコピーします。
- このワークフローは、ビルド前にローカル / 開発用バージョンを PyPI 向けの公開バージョンへ正規化できます。
- 公開には GitHub trusted publishing を使い、`pypa/gh-action-pypi-publish` を利用します。

## バージョン正規化

このリポジトリでは、`python/pyproject.toml` により豊かなローカル向けバージョン文字列を保持できます。例えば：

```toml
version = "0.0.1-beta.2+20260518"
```

PyPI は `+20260518` のようなローカルバージョン識別子を含むアップロードを許可しないため、このワークフローは `uv build` の前に**CI 内でのみ**バージョンを書き換えます。

例：

| リポジトリのバージョン | PyPI 用ビルドバージョン |
|---|---|
| `0.0.1-beta.2+20260518` | `0.0.1b2` |
| `0.0.1-rc.3+20260518` | `0.0.1rc3` |
| `0.0.1-alpha.4+20260518` | `0.0.1a4` |

現在の正規化ルール：

- `+` 以降をすべて削除
- `-alpha.N` -> `aN`
- `-beta.N` -> `bN`
- `-rc.N` -> `rcN`
- `-dev.N` -> `.devN`

これにより、git にはより説明的なバージョン文字列を残しつつ、PyPI には有効な PEP 440 の公開バージョンを渡せます。

## PyPI 設定

このワークフローは現在 **PyPI trusted publishing** を使用しているため、`PYPI_TOKEN` シークレットは**不要**です。

このリポジトリ用の PyPI trusted publisher を作成し、次の内容に向けてください：

- Repository: `VincentZyuApps/Qt-Kurarin`
- Workflow file: `.github/workflows/build.yml`
- Environment: `pypi`

### なぜ token が不要なのか

公開ジョブでは次を使用しています：

```yaml
permissions:
  id-token: write
```

そして：

```yaml
uses: pypa/gh-action-pypi-publish@release/v1
```

これは、GitHub Actions が公開時に OIDC ID トークンを要求し、PyPI 側では設定済みの trusted publisher に基づいてそのトークンを検証することを意味します。

### 旧来の token ベース方式を使いたい場合

このリポジトリを `winload` に近い挙動にしたいなら、公開ステップを token ベースのフローへ戻すこともできます。

その場合は次のリポジトリ secret が必要です：

- `PYPI_TOKEN`: PyPI API token。通常は project-scoped 権限の方が望ましいです

公開ステップはおおむね次のようになります：

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4

- name: Publish to PyPI
  working-directory: python
  env:
    UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
  run: uv publish --publish-url https://upload.pypi.org/legacy/
```

### 推奨

このリポジトリでは、trusted publishing をデフォルトにする方が適切です：

- 長期有効な PyPI token を GitHub secrets に保存しなくてよい
- secret 管理の手間が少ない
- 監査しやすい
- 現在の PyPI ベストプラクティスに沿っている
