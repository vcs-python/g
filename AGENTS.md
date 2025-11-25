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
- Proxies CLI arguments directly to the detected VCS binary
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
- Use namespace imports: `import typing as t`, `import logging`, etc.; avoid `from typing import ...`.
- Follow NumPy-style docstrings (see existing docstrings in `run` and pytest config requiring `pydocstyle` via ruff).
- Ruff is the source of truth for lint rules; see `pyproject.toml` for enabled checks (E, F, I, UP, A, B, C4, COM, EM, Q, PTH, SIM, TRY, PERF, RUF, D, FA100).
- Type checking is strict (`mypy --strict`); favor precise types and avoid `Any` unless necessary.

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
