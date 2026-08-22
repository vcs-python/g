# Contributing

Thanks for looking. A bug report with a reproduction — the directory layout
and the exact `g` invocation — is the most useful thing you can send; a
correction to somewhere the documentation misled you is a close second.

How this project writes prose — README, `CHANGES`, commit messages,
docstrings, source comments, and CLI/error text — is set out separately in
[WRITING.md](WRITING.md). Read that before changing any of it. The
constraints every change is held to, and the map of what is where, are in
[AGENTS.md](../AGENTS.md).

## Getting set up

Install [uv], then sync the dev and docs extras:

```console
$ uv sync --all-extras --dev
```

[uv]: https://github.com/astral-sh/uv

## The gates

CI is the order of record; every gate it runs has to pass before a change is
done.

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check . --fix --show-fixes
```

Type-check (`[tool.mypy] strict = true`):

```console
$ uv run mypy .
```

Test:

```console
$ uv run py.test
```

Documentation is a gate, not a courtesy. Examples in docstrings under
`src/g` and pages under `docs/` are executed by `pytest`/`py.test` — the
doctest flags live in `pyproject.toml`, so there is no separate doctest
step and a green test run is the proof. `README.md` is not included, so its
examples are never executed. Which blocks qualify, and the one mistake that
silently removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Ruff's isort config requires `from __future__ import annotations` in every
module (`required-imports`, backed by the `FA100` rule) — the linter, not
this file, catches a missing one. Import stdlib modules by namespace
(`import typing as t`, `import logging`) rather than `from typing import
…`; third-party packages may use `from X import Y`. Nothing enforces this
one — it is a convention, not a lint rule.

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

## Tests

Tests live in `tests/test_cli.py`, parametrized through a
`CommandLineTestFixture` `NamedTuple`. The autouse `setup` fixture in
`conftest.py` sets `G_IS_TEST=1` for every test, which makes `run()` return
the `subprocess.Popen` object instead of `None` so assertions can inspect
it — outside tests, `run()` always returns `None`.

CLI tests invoke real VCS binaries (at minimum `git`) rather than mocking
the subprocess call; use `tmp_path` and `monkeypatch` to simulate a
non-repo directory.

`find_repo_type()` requires a `.git`, `.svn`, or `.hg` **directory**. A git
worktree checkout's top-level `.git` is a file, not a directory, so
`test_command_line[g-cmd-inside-git-dir]` and its `--help` sibling fail
there even though nothing is broken. Work from a normal clone (not `git
worktree add`) to run the full suite green.

When subprocess output seems swallowed, set `G_IS_TEST=1` and call
`run(wait=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)` to capture
it for inspection.

Assert on `caplog.records` attributes, not string matching on `caplog.text`
— `caplog.record_tuples` cannot see `extra` fields. Scope capture with
`caplog.at_level(logging.DEBUG, logger="g")` — `g`'s modules log through
`logging.getLogger(__name__)`, so the logger name is the module's own
dotted path, `g` at the package root. Filter records rather than index by
position: `[r for r in caplog.records if hasattr(r, "vcs_cmd")]`.

## Documentation

Build once:

```console
$ make build_docs
```

Live-reloading preview at `http://localhost:8034`:

```console
$ make start_docs
```

From inside `docs/`, the same tasks are `just html` and `just start`; `just
--list` in `docs/` shows the rest (`watch`, `serve`, `linkcheck`,
`doctest`). `make build_docs` and `just html` both wrap
`sphinx-build`; nothing under `docs/_build` is hand-edited.

`AGENTS.md` and `CLAUDE.md` are excluded from the build
(`exclude_patterns` in `docs/conf.py`) — they are agent guidance, not site
pages. `make build_docs` catches a broken cross-reference; the test suite
does not, so build the docs before committing a documentation change.

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

1. Update `CHANGES` with the release notes.
2. Bump the version in `src/g/__about__.py` and `pyproject.toml`.
3. Commit the release files with the subject `Tag v<version>`.
4. Tag (`git tag v<version>`) and push the branch, then the tag
   (`git push --tags`).
5. CI builds and publishes to PyPI automatically over OIDC trusted
   publishing once the tag lands.

Full detail: [docs/project/releasing.md](../docs/project/releasing.md).

## Pull requests

One subject per pull request. Unrelated cleanup found along the way belongs
in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

Merge once you have the sign-off of one other developer. If you do not have
permission to merge, ask a maintainer to merge it for you.

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

This repository has no `SECURITY.md`. Please do not open a public issue for
a vulnerability — report it privately via [GitHub's security
advisories](https://github.com/vcs-python/g/security/advisories/new).
