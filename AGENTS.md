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

### Git Commit Standards

Format commit messages as:
```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject ≤50 chars (excluding any trailing `(#NN)` PR ref); wrap
body lines at ≤72 chars. Separate the `why:` and `what:` blocks with a
blank line.

Common commit types:
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev Dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)
- **ai(claude[command])**: Claude Code command changes

#### Release commits

Never create tags. Never push tags. The user handles tagging and tag
pushes (tags trigger the CI publish workflow).

Release commit subjects are plain and short: `Tag v<version>`. Put
the detailed why/what in the commit body. Don't use the
`Scope(type[detail]):` format for releases — don't bury the lede.

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

## Changelog Conventions

These rules apply when authoring entries in `CHANGES`, which is rendered as the Sphinx changelog page. Modeled on Django's release-notes shape — deliverables get titles and prose, not bullets. Older entries used a flat `### Section` + bullet shape; new entries follow the Django shape below.

**Release entry boilerplate.** Every release header is `## g X.Y.Z (YYYY-MM-DD)`. The file opens with a `## g X.Y.Z (unreleased)` placeholder block fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END PLACEHOLDER ... -->` HTML comments — new release entries land immediately below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open with the version as sentence subject (*"g X.Y.Z ships …"*) so the lead is self-contained when excerpted. Two to four sentences telling the reader what shipped and who cares — user-visible takeaways, not internal mechanism. Cross-reference detail docs with `{ref}` to keep the lead compact.

**Lead paragraphs are release-time material — off-limits to branches and PRs.** The unreleased entry carries no lead paragraph and no version summary: sections only (`### Breaking changes`, `### What's new` deliverables, `### Fixes`, …). Speaking for the release — what the version "is", "ships", or "focuses on" — is presumptuous before its scope is final; only the person cutting the release writes that, and only when the user explicitly asks to release. Never write or edit a lead from a feature branch, and never ask or imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`, every distinct deliverable gets a `#### Deliverable title (#NN)` heading naming it in user vocabulary, followed by 1-3 prose paragraphs explaining what shipped. Don't wrap a paragraph in `- ` — bullets are for enumerable lists, not paragraph containers. Cross-link detail docs (`See {ref}\`foo\` for details.`) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the deliverable, in user vocabulary?" If you can't answer in one sentence, the entry isn't ready. Mechanism (helper internals, byte counters, schema-validation locations) belongs in PR descriptions and code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`, `### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`, `### Development`. Dev tooling (helper scripts, internal automation) lives under `### Development`. For breaking changes, show the migration path with concrete inline code (e.g. a `# Before` / `# After` fenced code block). Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`, occasionally `### Documentation`) with 3+ genuinely small items use bullets — one line each, never paragraphs. If a bullet swells past two lines, promote it to a `#### Title (#NN)` heading with prose body.

**Anti-patterns.**

- Fragile metrics: token ceilings, third-party version pins, percent benchmarks, exact byte counts. Describe the *capability*, not the math.
- Internal jargon: private symbols (leading-underscore identifiers), algorithm names exposed for the first time, backend scaffolding.
- Walls of text dressed up as bullets.
- Buried breaking changes — they get their own subheading at the top of the entry.

**Always link autodoc'd APIs.** Any class, method, function, exception, or attribute that has its own rendered page must be cited via the appropriate role (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`) — never with plain backticks. Doc pages without explicit ref labels use `{doc}`. Plain backticks are correct for code syntax, env vars, parameter names, and file paths that aren't doc pages — anything without an autodoc destination.

**MyST roles.** Class references use `{class}`, methods use `{meth}`, functions use `{func}`, exceptions use `{exc}`, attributes use `{attr}`, internal anchors use `{ref}`, doc-path links use `{doc}`.

**Summarization style.** When a user asks "what changed in the latest version?" or similar, lead with the entry's lead paragraph (paraphrased if needed), followed by each `####` deliverable heading under `### What's new` with a one-sentence summary. Cite `(#NN)` only if the user asks for source links. Don't invent versions, dates, or numbers not present in `CHANGES`. Don't quote line numbers or file offsets — those shift as the file evolves.

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

## AI Slop Prevention

Treat AI slop as **review-hostile noise**, not as proof that text or
code is wrong. The goal is to maximize information density by removing
artifacts that make the repository harder to trust or navigate.

### The Anti-Slop Rubric

Before committing, audit all AI-assisted changes for these noise
patterns:

- **AI Signatures:** Remove "Generated by", footers, conversational
  filler ("Certainly!", "Here is..."), unexplained emojis (🤖, ✨), and
  AI-tool metadata.
- **Brittle References:** Avoid hard-coded line numbers, fragile
  file/test counts, dated "as of" claims, bare SHAs, and local
  absolute paths unless they are strict evidentiary artifacts (e.g.,
  benchmark logs).
- **Diff Narration:** Do not restate what moved, was renamed, or was
  removed in artifacts the downstream reader holds: code, docstrings,
  README, CHANGES, PR descriptions, or release notes. The diff and
  commit message already carry this history.
- **Branch-Internal Narrative:** Do not mention intermediate branch
  states, abandoned approaches, or "no longer" behavior unless users
  of a published release actually experienced the old state (**The
  Published-Release Test**).
- **Low-Value Scaffolding:** Remove ownerless TODOs (`TODO: revisit`),
  unused future-proofing, debug artifacts, and defensive wrappers that
  do not protect a currently reachable failure mode.
- **Prose Inflation:** Replace generic AI "tells" like *comprehensive,
  robust, seamless, production-ready, leverage, delve, tapestry,* and
  *best practices* with concrete descriptions of behavior,
  constraints, or trade-offs.
- **Coded Labels:** Write rules, options, and findings as plain
  imperatives. Don't tag them with codes like `[R1]`, `A1`, or
  `Option B` in artifacts a human reads — the reader shouldn't have to
  decode an index. Internal agent bookkeeping may use ids; shipped text
  may not.

### Preservation & Context

**When unsure, leave the text in place and ask.** Subjective cleanup
must never be a reason to remove load-bearing rationale.

- **Preserve the "Why":** You MUST NOT delete comments that document
  invariants, protocol constraints, platform quirks, security
  boundaries, and upstream workarounds.
- **Evidence is Immune:** Preserve exact counts, dates, and SHAs when
  they serve as evidence in benchmark results, release notes, stack
  traces, or lockfiles.
- **Behavior Over Inventory:** A useful description explains what
  changed for the *system or user*; it does not provide an inventory
  of files or functions the diff already shows.

### The Published-Release Test

Long-running branches accumulate tactical decisions — renames,
refactors, attempts-then-reverts. When deciding what counts as
branch-internal, use trunk or the parent branch as the baseline — not
intermediate states inside the current branch. Ask:

> Did users of the most recently published release ever experience
> this old name, old behavior, or bug?

If the answer is **no**, it is branch-internal narrative. Move it to
the commit message and describe only the final state in the artifact.

**Keep in shipped artifacts:**
- Deprecations and migration guides for symbols that actually shipped.
- `### Fixes` entries for bugs that affected users of a published
  release.
- Comments explaining *why the current code looks this way*
  (invariants, platform quirks) that make sense to a reader who never
  saw the previous version.

### Cleanup in Hindsight

When applying these rules retroactively from inside a feature branch,
first establish scope by diffing against the parent branch (or trunk)
to identify which commits this branch actually introduced. Then:

- **In-branch commits:** Prompt the user with two options: `fixup!`
  commits with `git rebase --autosquash` to address each causal commit
  at its source, or a single cleanup commit at branch tip.
- **Trunk/Parent commits:** Default to leaving them alone. Act only on
  explicit user instruction. If the user opts in, fold the cleanup
  into a single commit at branch tip; do not rewrite shared history.
- **Scope guard:** If cleaning prior slop would touch a colleague's
  work or expand the branch beyond its stated goal, stay in lane:
  protect the current goal and leave prior slop alone.

### Change Discipline

- Make the smallest coherent change that solves the verified problem;
  keep unrelated cleanup out of it.
- Reuse an existing file, component, helper, API, or test before adding
  a new one. Modify in place when the change fits the file's
  responsibility.
- Keep new APIs private until a caller outside the module needs them.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized high-touch module — not
  for a single-use helper or a one-line re-export.

### Keep Instructions Lean

Treat this file like code and prune it.

- Delete a line whose removal would not cause a mistake.
- Move multi-step procedures into skills, path-specific rules into
  nested AGENTS.md files, and hard limits into hooks or CI.
- Keep only non-obvious, broadly applicable defaults here. Anything a
  reader can infer from the code, a manifest, or a linter does not
  belong.
