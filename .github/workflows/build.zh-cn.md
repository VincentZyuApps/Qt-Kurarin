# 构建与发布工作流

> **[📖 English](build.md)**
> **[📖 简体中文(大陆)](build.zh-cn.md)**
> **[📖 日本語](build.jp.md)**

这个仓库为 `python/` 目录中的 Python 包使用了一套小型的、由 commit message 驱动的工作流。

## 关键词

| Commit 信息中的关键词 | 构建 wheel/sdist | 发布到 PyPI |
|---|:---:|:---:|
| `build action` | ✅ | ❌ |
| `publish pypi` | ✅ | ✅ |
| `pypi publish` | ✅ | ✅ |

## 示例

```bash
# 仅构建
git commit --allow-empty -m "ci: verify package build (build action)"

# 构建并发布到 PyPI
git commit --allow-empty -m "release: v0.0.1-beta.1 (publish pypi)"
```

## 说明

- Pull request 总是会运行构建任务，但不会发布。
- 包版本从 `python/pyproject.toml` 读取。
- 仓库 README 位于仓库根目录；CI 会在构建前将其复制到 `python/README.md`。
- 该工作流可以在构建前把本地 / 开发版本规范化为适合 PyPI 的公开版本。
- 发布使用 GitHub trusted publishing，通过 `pypa/gh-action-pypi-publish` 完成。

## 版本规范化

这个仓库可以在 `python/pyproject.toml` 中保留更丰富的本地版本字符串，例如：

```toml
version = "0.0.1-beta.2+20260518"
```

PyPI 不允许上传带有 `+20260518` 这类本地版本标识符的版本，因此该工作流会在 `uv build` 之前**仅在 CI 内部**重写版本号。

示例：

| 仓库中的版本 | PyPI 构建版本 |
|---|---|
| `0.0.1-beta.2+20260518` | `0.0.1b2` |
| `0.0.1-rc.3+20260518` | `0.0.1rc3` |
| `0.0.1-alpha.4+20260518` | `0.0.1a4` |

当前规范化规则：

- 删除 `+` 之后的所有内容
- `-alpha.N` -> `aN`
- `-beta.N` -> `bN`
- `-rc.N` -> `rcN`
- `-dev.N` -> `.devN`

这意味着你可以在 git 中保留更具描述性的版本字符串，同时 PyPI 仍然会收到符合 PEP 440 的公开版本。

## PyPI 设置

这个工作流当前使用的是 **PyPI trusted publishing**，因此你**不**需要 `PYPI_TOKEN` 密钥。

为这个仓库创建一个 PyPI trusted publisher，并把它指向：

- Repository: `VincentZyuApps/Qt-Kurarin`
- Workflow file: `.github/workflows/build.yml`
- Environment: `pypi`

### 为什么不需要 token

发布任务使用了：

```yaml
permissions:
  id-token: write
```

以及：

```yaml
uses: pypa/gh-action-pypi-publish@release/v1
```

这意味着 GitHub Actions 会在发布时请求一个 OIDC 身份令牌，而 PyPI 会根据你在 PyPI 端配置的 trusted publisher 来验证这个令牌。

### 如果你更喜欢旧的 token 风格

如果你希望这个仓库的行为更像 `winload`，可以把发布步骤切回基于 token 的流程。

那么你就需要一个仓库密钥：

- `PYPI_TOKEN`: 一个 PyPI API token，通常更建议使用 project-scoped 权限

发布步骤看起来会更像这样：

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4

- name: Publish to PyPI
  working-directory: python
  env:
    UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
  run: uv publish --publish-url https://upload.pypi.org/legacy/
```

### 建议

对于这个仓库，trusted publishing 是更好的默认选择：

- 不需要在 GitHub secrets 中存放长期有效的 PyPI token
- 更少的密钥管理工作
- 更容易审计
- 更符合当前 PyPI 的最佳实践
