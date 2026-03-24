# Code Style

## Formatting

g uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```console
$ uv run ruff format .
```

```console
$ uv run ruff check . --fix
```

## Type Checking

[mypy](https://mypy-lang.org/) is used for static type checking.

```console
$ uv run mypy
```
