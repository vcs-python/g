# AGENTS.md

This file provides guidance to AI agents (including Claude Code, Cursor, and other LLM-powered tools) when working with code in this repository. The tooling and docs rely on the gp-libs ecosystem; treat gp-libs as the shared dev toolkit that underpins this project.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests MUST pass for code to be considered complete and working
- Never describe code as "working as expected" if there are ANY failing tests
- Even if specific feature tests pass, failing tests elsewhere indicate broken functionality
- Changes that break existing tests must be fixed before considering implementation complete
- A successful implementation must pass linting, type checking, AND all existing tests

## Project Overview

g is a lightweight CLI wrapper that proxies to the current directory's VCS command (git, svn, or hg). It auto-detects the repo type, forwards user arguments, and exits after invoking the native tool. The project lives in the gp-libs family of git-pull utilities and uses gp-libs packages for docs and development helpers.

Key features:
- Detects VCS by walking parent directories and mapping `.git`, `.svn`, or `.hg`
- Proxies CLI arguments to the detected VCS binary (--version/-V is handled by g)
- Minimal surface area: primary logic lives in `src/g/__init__.py`
- Test fixtures cover CLI behavior for both repo and non-repo directories

## Development Environment

This project uses:
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management and execution
- [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://github.com/python/mypy) for type checking
- [pytest](https://docs.pytest.org/) (invoked as `py.test`) for testing
- [gp-libs](https://gp-libs.git-pull.com/) for shared Sphinx/test helpers (included in dev/docs extras)

## Common Commands

### Setting Up Environment

```bash
# Install all dev and doc dependencies
uv sync --all-extras --dev
```

### Running Tests

```bash
# Run full suite
make test
# or directly
uv run py.test

# Watch tests (pytest-watcher)
make start  # runs tests once then ptw .

# Watch tests via entr (requires entr(1))
make watch_test
```

### Linting and Type Checking

```bash
# Lint and format with ruff
uv run ruff check .
uv run ruff format .

# make targets
make ruff
make ruff_format
make watch_ruff

# Type checking
uv run mypy .
make mypy
make watch_mypy
```

### Documentation

```bash
# Build docs
make build_docs

# Live docs server with autoreload
make start_docs

# Docs design assets
make design_docs
```

## Code Architecture

```
src/g/__init__.py
  ├─ find_repo_type(): detect VCS by walking parent directories
  ├─ run(): CLI entrypoint; proxies args to detected VCS, honors G_IS_TEST
  └─ DEFAULT + vcspath_registry helpers

tests/test_cli.py
  └─ Parametrized CLI tests for git/non-repo scenarios
```

## Testing Strategy

- Tests live in `tests/test_cli.py` and use `pytest` with parametrized fixtures.
- `G_IS_TEST` env flag forces `run()` to return the subprocess so output can be asserted; set when modifying run logic.
- CLI tests rely on actual VCS binaries (e.g., `git`) being available on PATH. If adding tests for svn/hg, ensure binaries are installed or skip appropriately.
- Use `tmp_path` and `monkeypatch` to simulate non-repo directories instead of mocks where possible.
- Prefer pytest-watcher (`make start`) for TDD loops; for file-watch without ptw, use `make watch_test` (requires entr).

## Coding Standards

- Include `from __future__ import annotations` at the top of Python modules.
- Use namespace imports for stdlib: `import typing as t`, `import logging`, etc.; third-party packages may use `from X import Y`.
- Follow NumPy-style docstrings (see existing docstrings in `run` and pytest config requiring `pydocstyle` via ruff).
- Ruff is the source of truth for lint rules; see `pyproject.toml` for enabled checks (E, F, I, UP, A, B, C4, COM, EM, Q, PTH, SIM, TRY, PERF, RUF, D, FA100).
- Type checking is strict (`mypy --strict`); favor precise types and avoid `Any` unless necessary.

## Logging Standards

These rules guide future logging changes; existing code may not yet conform.

### Logger setup

- Use `logging.getLogger(__name__)` in every module
- Add `NullHandler` in library `__init__.py` files
- Never configure handlers, levels, or formatters in library code — that's the application's job

### Structured context via `extra`

Pass structured data on every log call where useful for filtering, searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
|-----|------|---------|
| `vcs_cmd` | `str` | VCS command line |
| `vcs_type` | `str` | VCS type (git, svn, hg) |
| `vcs_url` | `str` | repository URL |
| `vcs_exit_code` | `int` | VCS process exit code |
| `vcs_repo_path` | `str` | local repository path |

**Heavy/optional keys** (DEBUG only, potentially large):

| Key | Type | Context |
|-----|------|---------|
| `vcs_stdout` | `list[str]` | VCS stdout lines (truncate or cap; `%(vcs_stdout)s` produces repr) |
| `vcs_stderr` | `list[str]` | VCS stderr lines (same caveats) |

Treat established keys as compatibility-sensitive — downstream users may build dashboards and alerts on them. Change deliberately.

### Key naming rules

- `snake_case`, not dotted; `vcs_` prefix
- Prefer stable scalars; avoid ad-hoc objects
- Heavy keys (`vcs_stdout`, `vcs_stderr`) are DEBUG-only; consider companion `vcs_stdout_len` fields or hard truncation (e.g. `stdout[:100]`)

### Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:
- Deferred string interpolation: skipped entirely when level is filtered
- Aggregator message template grouping: `"Running %s"` is one signature grouped ×10,000; f-strings make each line unique

When computing `val` itself is expensive, guard with `if logger.isEnabledFor(logging.DEBUG)`.

### stacklevel for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel `code.filepath` point to the real caller. Verify whenever call depth changes.

### LoggerAdapter for persistent context

For objects with stable identity (Repository, Remote, Sync), use `LoggerAdapter` to avoid repeating the same `extra` on every call. Lead with the portable pattern (override `process()` to merge); `merge_extra=True` simplifies this on Python 3.13+.

### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics, VCS I/O | VCS command + stdout, URL parsing steps |
| `INFO` | Repository lifecycle, user-visible operations | Repository cloned, sync completed |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Deprecated VCS option, unrecognized remote |
| `ERROR` | Failures that stop an operation | VCS command failed, invalid URL |

Config discovery noise belongs in `DEBUG`; only surprising/user-actionable config issues → `WARNING`.

### Message style

- Lowercase, past tense for events: `"repository cloned"`, `"vcs command failed"`
- No trailing punctuation
- Keep messages short; put details in `extra`, not the message string

### Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not** re-raising
- Use `logger.error(..., exc_info=True)` when you need the traceback outside an `except` block
- Avoid `logger.exception()` followed by `raise` — this duplicates the traceback. Either add context via `extra` that would otherwise be lost, or let the exception propagate

### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:
- Scope capture: `caplog.at_level(logging.DEBUG, logger="g.cli")`
- Filter records rather than index by position: `[r for r in caplog.records if hasattr(r, "vcs_cmd")]`
- Assert on schema: `record.vcs_exit_code == 0` not `"exit code 0" in caplog.text`
- `caplog.record_tuples` cannot access extra fields — always use `caplog.records`

### Avoid

- f-strings/`.format()` in log calls
- Unguarded logging in hot loops (guard with `isEnabledFor()`)
- Catch-log-reraise without adding new context
- `print()` for diagnostics
- Logging secret env var values (log key names only)
- Non-scalar ad-hoc objects in `extra`
- Requiring custom `extra` fields in format strings without safe defaults (missing keys raise `KeyError`)

## Doctests

**All functions and methods MUST have working doctests.** Doctests serve as both documentation and tests.

**CRITICAL RULES:**
- Doctests MUST actually execute - never comment out function calls or similar
- Doctests MUST NOT be converted to `.. code-block::` as a workaround (code-blocks don't run)
- If you cannot create a working doctest, **STOP and ask for help**

**Available tools for doctests:**
- `doctest_namespace` fixtures: `tmp_path`
- Ellipsis for variable output: `# doctest: +ELLIPSIS`
- Update `conftest.py` to add new fixtures to `doctest_namespace`

**`# doctest: +SKIP` is NOT permitted** - it's just another workaround that doesn't test anything. If a VCS binary might not be installed, use proper skip markers in pytest.

**Using fixtures in doctests:**
```python
>>> from g import find_repo_type
>>> find_repo_type('/some/git/repo')  # doctest: +ELLIPSIS
'git'
```

**When output varies, use ellipsis:**
```python
>>> import pathlib
>>> pathlib.Path.cwd()  # doctest: +ELLIPSIS
PosixPath('...')
```

## Debugging Tips

- Add logging with `logging` configured in `run`; keep output minimal because the CLI forwards to underlying VCS.
- When diagnosing repo detection, log the path iteration in `find_repo_type` or unit-test with synthetic directory trees.
- If subprocess output is swallowed, run with `G_IS_TEST=1` and `wait=True` to capture stdout/stderr in tests.

## References

- Documentation: https://g.git-pull.com/
- API: https://g.git-pull.com/api.html
- Changelog: https://g.git-pull.com/history.html
- Repository: https://github.com/vcs-python/g
- Shared tooling (gp-libs): https://gp-libs.git-pull.com/
