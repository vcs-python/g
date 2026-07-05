# Code Style

Use this page when you are changing g itself and want the same local checks CI
expects.

## Formatting

g uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```console
$ uv run ruff check . --fix
```

```console
$ uv run ruff format .
```

## Type Checking

[mypy](https://mypy-lang.org/) is used for static type checking.

```console
$ uv run mypy .
```
