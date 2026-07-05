# Code Style

Use this page when you are changing g itself and want the same local checks CI
expects.

## Formatting

Run [ruff](https://github.com/astral-sh/ruff) before committing Python changes.

```console
$ uv run ruff check . --fix
```

```console
$ uv run ruff format .
```

## Type Checking

Run [mypy](https://mypy-lang.org/) for static type checking.

```console
$ uv run mypy .
```
