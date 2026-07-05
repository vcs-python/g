# Development

Use this page when you want to change g itself. If you only want to install and
run the command, start with {doc}`/quickstart`.

## Bootstrap the project

Install [git] and [uv].

Clone:

```console
$ git clone https://github.com/vcs-python/g.git
```

```console
$ cd g
```

Install packages:

```console
$ uv sync --all-extras --dev
```

[installation documentation]: https://docs.astral.sh/uv/getting-started/installation/
[git]: https://git-scm.com/

## Tests

```console
$ uv run py.test
```

The Makefile wrapper runs the same test command.

```console
$ make test
```

## Automatically run tests on file save

1. `make start` (via [pytest-watcher])
2. `make watch_test` (requires installing [entr(1)])

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher

## Documentation

Default preview server: http://localhost:8034

[sphinx-autobuild] builds the docs, watches for file changes, and launches a
server.

From home directory: `make start_docs`
From inside `docs/`: `make start`

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation

`cd docs/` and `make html` to build. `make serve` to start http server.

Helpers:
`make build_docs`, `make serve_docs`

Rebuild docs on file change: `make watch_docs` (requires [entr(1)])

Rebuild docs and run server via one terminal: `make dev_docs` (requires above, and a
`make(1)` with `-J` support, e.g. GNU Make)

## Formatting / Linting

### Linting and formatting

The project uses [ruff] to handle formatting, sorting imports and linting.

````{tab} Command

uv:

```console
$ uv run ruff check .
```

If you set up manually:

```console
$ ruff check .
```

````

````{tab} make

```console
$ make ruff
```

````

````{tab} Watch

```console
$ make watch_ruff
```

requires [`entr(1)`].

````

````{tab} Fix files

uv:

```console
$ uv run ruff check . --fix
```

If you set up manually:

```console
$ ruff check . --fix
```

````

#### Code formatting

Use [ruff format] for formatting.

````{tab} Command

uv:

```console
$ uv run ruff format .
```

If you set up manually:

```console
$ ruff format .
```

````

````{tab} make

```console
$ make ruff_format
```

````

### Type checking

Use [mypy] for static type checking.

````{tab} Command

uv:

```console
$ uv run mypy .
```

If you set up manually:

```console
$ mypy .
```

````

````{tab} make

```console
$ make mypy
```

````

````{tab} Watch

```console
$ make watch_mypy
```

requires [`entr(1)`].
````

## Releasing

[uv] handles virtualenv creation, package requirements, versioning,
building, and publishing. There is no `setup.py` or requirements file.

See {doc}`/project/releasing` before preparing a release.

[uv]: https://github.com/astral-sh/uv
[entr(1)]: http://eradman.com/entrproject/
[`entr(1)`]: http://eradman.com/entrproject/
[ruff format]: https://docs.astral.sh/ruff/formatter/
[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
