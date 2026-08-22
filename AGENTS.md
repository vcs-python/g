# AGENTS.md

g is a lightweight CLI wrapper: it detects the current directory's VCS
(git, svn, or hg) and proxies your arguments straight to it.

Follow the conventions already in the tree, and keep a change scoped to what
was asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/g/__init__.py` | Everything: `find_repo_type()`, `create_parser()`, `run()` (console-script entry point) |
| `src/g/__about__.py` | Package metadata (`__version__`, URLs); exec'd by `docs/conf.py` |
| `tests/test_cli.py` | Parametrized CLI tests |
| `conftest.py` | Autouse fixture setting `G_IS_TEST=1` |
| `docs/` | Sphinx (MyST) site; `docs/cli/index.md` is the CLI reference |
| `CHANGES` | Changelog, rendered as the docs history page |
| `Makefile`, `justfile`, `docs/justfile` | Task runners wrapping `uv`/`just` |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, commit messages, docstrings,
  source comments, logging, and CLI/error text:
  [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one. Keep
  a new API private until a caller outside the module needs it.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES` entry
  for every change to the public API, CLI, configuration, or output.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.
- `find_repo_type()` requires a `.git`/`.svn`/`.hg` **directory**; it will
  not detect a repo from a git worktree checkout, whose top-level `.git` is
  a file. This is a real limitation, not a bug in a test.
- Keep this file lean: delete a line whose removal would not cause a
  mistake; push a multi-step procedure into a skill and a path-specific
  rule into a nested `AGENTS.md`.

## References

- Documentation: https://g.git-pull.com/
- API: https://g.git-pull.com/api.html
- Changelog: https://g.git-pull.com/history.html
- Repository: https://github.com/vcs-python/g
- Shared tooling (gp-libs): https://gp-libs.git-pull.com/
