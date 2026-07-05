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

Run tests once, then keep watching with [pytest-watcher]:

```console
$ make start
```

Watch through [entr(1)] if you have it installed:

```console
$ make watch_test
```

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher

## Documentation

Default preview server: http://localhost:8034

[sphinx-autobuild] builds the docs, watches for file changes, and launches a
server.

From the project root:

```console
$ make start_docs
```

From inside `docs/`:

```console
$ make start
```

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation

Enter the docs directory:

```console
$ cd docs
```

Build the docs:

```console
$ make html
```

Start the HTTP server:

```console
$ make serve
```

Project-root helpers run the same docs tasks:

```console
$ make build_docs
```

```console
$ make serve_docs
```

Rebuild docs on file change with [entr(1)]:

```console
$ make watch_docs
```

Rebuild docs and run the server through one terminal when your [GNU Make] has
`-J` support:

```console
$ make dev_docs
```

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
[GNU Make]: https://www.gnu.org/software/make/
[ruff format]: https://docs.astral.sh/ruff/formatter/
[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
