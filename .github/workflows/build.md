# Build & Publish Workflow

> **[📖 English](build.md)**
> **[📖 简体中文(大陆)](build.zh-cn.md)**
> **[📖 日本語](build.jp.md)**

This repository uses a small commit-message-driven workflow for the Python package in `python/`.

## Keywords

| Keyword in commit message | Build wheel/sdist | Publish to PyPI |
|---|:---:|:---:|
| `build action` | ✅ | ❌ |
| `publish pypi` | ✅ | ✅ |
| `pypi publish` | ✅ | ✅ |

## Examples

```bash
# Build only
git commit --allow-empty -m "ci: verify package build (build action)"

# Build + publish to PyPI
git commit --allow-empty -m "release: v0.0.1-beta.1 (publish pypi)"
```

## Notes

- Pull requests always run the build job, but never publish.
- The package version is read from `python/pyproject.toml`.
- The repository README lives at the repository root; CI copies it into `python/README.md` before building.
- The workflow can normalize a local/developer version into a PyPI-safe public version before building.
- Publishing uses GitHub trusted publishing via `pypa/gh-action-pypi-publish`.

## Version normalization

This repository may keep a richer local version string in `python/pyproject.toml`, for example:

```toml
version = "0.0.1-beta.2+20260518"
```

PyPI does not allow uploading local version identifiers such as `+20260518`, so the workflow rewrites the version **inside CI only** before `uv build`.

Examples:

| Repository version | PyPI build version |
|---|---|
| `0.0.1-beta.2+20260518` | `0.0.1b2` |
| `0.0.1-rc.3+20260518` | `0.0.1rc3` |
| `0.0.1-alpha.4+20260518` | `0.0.1a4` |

Current normalization rules:

- remove anything after `+`
- `-alpha.N` -> `aN`
- `-beta.N` -> `bN`
- `-rc.N` -> `rcN`
- `-dev.N` -> `.devN`

That means you can keep a more descriptive version in git, while PyPI still receives a valid PEP 440 public version.

## PyPI setup

This workflow currently uses **PyPI trusted publishing**, so you do **not** need a `PYPI_TOKEN` secret.

Create a PyPI trusted publisher for this repository and point it at:

- Repository: `VincentZyuApps/Qt-Kurarin`
- Workflow file: `.github/workflows/build.yml`
- Environment: `pypi`

### Why no token is needed

The publish job uses:

```yaml
permissions:
  id-token: write
```

and:

```yaml
uses: pypa/gh-action-pypi-publish@release/v1
```

That means GitHub Actions requests an OIDC identity token at publish time, and PyPI verifies that token against the trusted publisher you configured on the PyPI side.

### If you prefer the old token-based style

If you want this repository to behave more like `winload`, you can switch the publish step back to a token-based flow.

Then you would need a repository secret:

- `PYPI_TOKEN`: a PyPI API token, usually with project-scoped access preferred

And the publish step would look more like:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4

- name: Publish to PyPI
  working-directory: python
  env:
    UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
  run: uv publish --publish-url https://upload.pypi.org/legacy/
```

### Recommendation

For this repository, trusted publishing is the better default:

- no long-lived PyPI token stored in GitHub secrets
- less secret management
- easier to audit
- aligned with current PyPI best practice
