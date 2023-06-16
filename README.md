# patch1337

[![PyPI Status](https://img.shields.io/pypi/status/patch1337?logo=PyPI)](https://pypi.python.org/pypi/patch1337)
[![PyPI version](https://img.shields.io/pypi/v/patch1337.svg?logo=PyPI)](https://pypi.python.org/pypi/patch1337)
[![linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&label=linting)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=Python)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Cross-platform 1337 patcher in Python. Initially designed to be used for [nvidia-patch](https://github.com/keylase/nvidia-patch).

## Installation

### From pypi

Suggested to install via [pipx](https://pypa.github.io/pipx) with:

```bash
pipx install patch1337
```

or pip with:

```bash
pip install patch1337
```

### From repo

Clone the repo with:

```bash
git clone https://github.com/OMEGARAZER/patch1337.git
cd ./patch1337
```

Suggested to install via [pipx](https://pypa.github.io/pipx) with:

```bash
pipx install -e .
```

or pip with:

```bash
pip install -e .
```

## Running

Once installed the patcher can be run with:

```bash
patch1337
```

When no arguments are passed the defaults settings will patch `nvEncodeAPI` and `nvEncodeAPI64` in the current directory.
To specify locations pass patch files with `-p` and patch targets with `-t`.

```bash
patch1337 --patch nvencodeapi.1337 --target C:\Windows\SysWOW64\nvEncodeAPI.dll -offset true
```

## Arguments

There are three arguments that can be passed to the patcher:

- `-p, --patch`
    - The path to a 1337 patch file.
- `-t, --target`
    - The path to the target file to patch.
- `-o, --offset`
    - Whether to apply the x64dbg offset (true by defualt)
- `-v`
    - Increase verbosity to debug output

Each can be specified multiple times to patch multiple files at once like this:

```bash
patch1337 --patch nvencodeapi.1337 --target nvEncodeAPI.dll -offset true --patch nvencodeapi64.1337 --target nvEncodeAPI64.dll -offset true
```
