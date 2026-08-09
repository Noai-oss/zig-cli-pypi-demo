# zig-cli-pypi-demo

A minimal example of building a Zig CLI and distributing it on PyPI as
platform-specific wheels for Windows, macOS, and Linux.

## Install

Install from PyPI:

```console
pip install zig-cli-pypi-demo
zypi-demo
```

You can also run it as a Python module:

```console
python -m zypi_demo
```

The Python launcher and executable lookup logic are adapted from
[Ruff](https://github.com/astral-sh/ruff/tree/6f86de2eb6363f77a314998c414ac8b53849b92f/python/ruff).

## Supported platforms

- Windows x86-64 (`win_amd64`)
- macOS x86-64 (`macosx_11_0_x86_64`)
- macOS Arm64 (`macosx_11_0_arm64`)
- Linux x86-64 (`manylinux_2_17_x86_64`)
- Linux Arm64 (`manylinux_2_17_aarch64`)

Python 3.10 is the minimum supported version.

## Development

To build the project, install Zig 0.16.0 and
[uv](https://docs.astral.sh/uv/).

```console
uv sync
uv run zypi-demo
```

Build all five wheels into `dist/`:

```console
uv run python make_wheels.py
```

> **Windows cross-build note:** When building Linux or macOS wheels on Windows,
> `make_wheels.py` records mode `0755` in the wheel metadata because Windows
> `chmod` cannot set Unix executable bits.

Pass `--target` to build a specific target. Only wheels are built; no source
distribution (sdist) is produced.

## Publish

Before publishing, set `UV_PUBLISH_TOKEN`, make sure the version matches in
`pyproject.toml` and `build.zig.zon`, and commit all changes. Then run:

```console
uv run python pypi_publish.py 0.0.1
```

The script checks that the versions match and the Git working tree is clean,
builds and validates all five wheels, creates and pushes the version tag, and
then publishes the wheels to PyPI.
