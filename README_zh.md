# zig-cli-pypi-demo

[English](README.md)

用 Zig 编写命令行工具，并以 Windows、macOS 和 Linux 平台 wheel 发布到 PyPI 的最小示例。

## 安装

需要 Python 3.10 或更高版本。

```console
pip install zig-cli-pypi-demo
zypi-demo
```

也可以通过 Python 模块运行：

```console
python -m zypi_demo
```

Python 启动器和可执行文件查找逻辑改编自
[Ruff](https://github.com/astral-sh/ruff/tree/6f86de2eb6363f77a314998c414ac8b53849b92f/python/ruff)。

## 支持平台

- Windows x86-64（`win_amd64`）
- macOS x86-64（`macosx_11_0_x86_64`）
- macOS Arm64（`macosx_11_0_arm64`）
- Linux x86-64（`manylinux_2_17_x86_64`）
- Linux Arm64（`manylinux_2_17_aarch64`）

## 开发与构建

安装 Zig 0.17.0 和 [uv](https://docs.astral.sh/uv/)，然后运行：

```console
uv sync
uv run zypi-demo
```

将五个平台的 wheel 构建到 `dist/`：

```console
uv run python make_wheels.py
```

可用 `--target` 指定构建目标。脚本只生成 wheel，不生成源码包（sdist）。

在 Windows 上构建 Linux/macOS wheel 时，脚本会将包内可执行文件条目的权限设为 `0755`，因为 Windows 的 `chmod` 无法设置 Unix 执行权限。

## 发布

设置 `UV_PUBLISH_TOKEN`，确保 `pyproject.toml`、`build.zig.zon` 与命令参数中的版本一致，并提交所有修改：

```console
uv run python pypi_publish.py 0.0.1
```

脚本检查版本、工作区和本地及远程标签，构建并校验五个平台的 wheel，先上传 PyPI，成功后再创建并推送版本标签。
