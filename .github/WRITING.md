# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, commit messages, CLI and error-message text,
docstrings, source comments, logging, and the Sphinx docs under `docs/`
— every surface a reader reaches.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was built
that way belongs in the commit message, which is timestamped and attached to
the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks. Prefer
short declarative sentences, one operational fact each. Do not explain Python
to Python developers; do explain this project's semantics.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                            |
| --------------------------------- | --------------------------------- |
| "We added…"                      | "`g` now proxies…"                |
| "New and improved"               | "`g` now…"                        |
| "powerful", "seamless"           | state the capability              |
| "easily", "simply", "just"       | omit                              |
| "simple", "obvious", "intuitive" | omit                              |
| "robust"                         | name the failure that is handled  |
| "comprehensive"                  | name what is covered              |
| "production-ready"               | state the guarantee               |
| "optimized", "blazingly fast"    | give the magnitude                |
| "various fixes"                  | name the components               |
| "under the hood"                 | omit unless observable            |
| "please note that", "note that"  | state the fact                    |
| "leverage", "utilize"            | "use"                             |
| "delve into"                     | "read", or omit                   |
| "best practices"                 | name the practice                 |
| "in order to"                    | "to"                              |

## Who you are writing for

The default reader works at a shell prompt inside a checkout and runs `g`
where they would otherwise type `git`, `svn`, or `hg`. They are fluent in
their own VCS — status, commit, log, diff — but you cannot assume they read
Python or know g's internals: `find_repo_type()`, the `vcspath_registry`
marker mapping, or the `G_IS_TEST` escape hatch the tests use.

A second, smaller reader writes Python: they call `run()` directly, build on
`create_parser()`, or contribute to g itself. Serve them too, but mark their
material opt-in — "for the rarer cases", "internal" — so the default reader
knows they can stop. Never make the common case pay a comprehension tax for
the advanced one.

Rules that follow:

- **Second person, present tense, active.** "You run `g status`", not "the
  command is proxied". Address the reader who is doing the thing.
- **Concept before mechanics.** Open by saying what g *does* for the reader —
  one command that becomes the right VCS command. The generated option
  listing, the marker table, and the exit behaviour are the last details they
  need, not the first. A page that opens with argparse output has buried the
  idea under its plumbing.
- **Say when they can stop.** g has no configuration; most pages owe the
  reader one reassurance up front — run `g` where you'd run your VCS, and
  you're done. Let a skimmer leave after one sentence.
- **Grant permission, do not demand attention.** "Reach for this when…", "for
  the rarer cases" — tell readers they are in the right place without
  implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the everyday
  command, then the one flag g intercepts (`--version`/`-V`), then how
  detection works, then the Python entry points. Each step is for a smaller
  audience than the last.
- **Lean on the pipeline.** The reader's mental model is a straight line:
  current directory → walk up the parents → a `.git`, `.svn`, or `.hg`
  marker → the matching VCS command, with arguments forwarded. Reinforce
  that chain whenever explaining detection or dispatch; it is the whole
  tool.
- **Name the trade-off.** If a call costs something, say so and say what it
  buys — `--version`/`-V` never reaches the underlying VCS, and g's own exit
  status does not mirror the wrapped command's (see
  [CLI and error messages](#cli-and-error-messages)). State it; do not sell
  it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its
  directory marker or argparse detail; name the concept — detection,
  forwarding. The mechanics vocabulary — the marker-to-command table, the
  generated option reference — belongs in the CLI reference, and only there.

## README

A README is the shortest path from "what is this?" to competent use, not the
project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command or snippet before anything the reader can skip. A
logo, a mission statement, a comparison matrix and three paragraphs of
history in front of the install line all cost the same thing.

State the minimum Python version in prose, not only in badges.
`requires-python` in `pyproject.toml` is the authority; the README must
agree with it.

Document the semantic model, not the flag list. `--help` already enumerates
flags (or, here, forwards straight to the VCS's own `--help` — see
[CLI and error messages](#cli-and-error-messages)); what it cannot say is
what goes to stdout versus stderr and what a non-zero exit means.

State defaults explicitly — defaults are API. State negative guarantees
where they exist: g has no configuration file, makes no network calls of its
own, and never invokes anything but the VCS binary the marker maps to. They
establish boundaries faster than any amount of description.

Headings stay conventional and stable, because people deep-link them. Badges
are few and load-bearing.

## CLI and error messages

g's whole surface is one command, so its error-message and exit-status
contract carries more weight than its flag list. This section is precise on
purpose; verify a claim against the source before repeating it elsewhere.

**Only `--version`/`-V` is intercepted.** g checks whether the first argument
is `--version` or `-V` before doing anything else; if so, it prints
`g <version>` to stdout and exits `0`. Every other argument — including
`-h`/`--help` — is forwarded to the detected VCS untouched. `g --help` runs
`git --help` (or `svn`/`hg`), not g's own help text.

**No detection, no error.** Outside any `.git`, `.svn`, or `.hg` directory, g
writes `No VCS found in current directory.` to stderr through the `logging`
module and returns — this is not treated as a failure. Keep that message
string exact; docs and tests refer to it literally.

**Output is inherited, not reshaped.** g does not capture, filter, or
reformat the VCS's own stdout or stderr. The subprocess inherits the
parent's file descriptors, so a proxied command prints exactly what the VCS
itself would print, byte for byte.

**g's own exit status does not mirror the wrapped command's.** After a
proxied VCS command completes, `run()` returns `None` and the process exits
`0` regardless of whether the VCS itself failed — a failing `git` command
still leaves `g` reporting success to the shell. If the mapped binary is
missing entirely (a `.hg` marker with no `hg` on `PATH`), `subprocess.Popen`
raises `FileNotFoundError`, an unhandled traceback prints to stderr, and the
process exits `1`. State this behaviour plainly wherever it comes up; do not
imply it is a bug being fixed or a feature being sold.

## Logging

g logs through the standard `logging` module rather than `print()`; log
output is a surface downstream tooling can parse, so treat its shape like
any other documented output.

### Structured context via `extra`

Pass structured data on a log call whenever it helps filtering, searching, or
test assertions.

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
| `vcs_stdout` | `list[str]` | VCS stdout lines (truncate or cap) |
| `vcs_stderr` | `list[str]` | VCS stderr lines (same caveats) |

Treat these keys as compatibility-sensitive — downstream users may build
dashboards and alerts on them. Change them deliberately: `snake_case`, not
dotted, `vcs_` prefix, scalars over ad-hoc objects.

### Lazy formatting

`logger.debug("msg %s", val)`, not an f-string. Deferred interpolation is
skipped entirely when the level is filtered, and a `"Running %s"` template
groups as one signature in an aggregator instead of one unique line per call.
Guard an expensive `val` with `if logger.isEnabledFor(logging.DEBUG)`.

### stacklevel and persistent context

Increment `stacklevel` for each wrapper layer so `%(filename)s:%(lineno)d`
points at the real caller; verify whenever call depth changes. For an object
with stable identity, prefer a `LoggerAdapter` (override `process()` to
merge `extra`) over repeating the same `extra` on every call.

### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics, VCS I/O | VCS command + stdout, URL parsing steps |
| `INFO` | Repository lifecycle, user-visible operations | Repository cloned, sync completed |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Deprecated VCS option, unrecognized remote |
| `ERROR` | Failures that stop an operation | VCS command failed, invalid URL |

Config discovery noise belongs in `DEBUG`; only a surprising or
user-actionable config issue goes to `WARNING`.

### Message style

Lowercase, past tense for events — `"repository cloned"`, `"vcs command
failed"` — no trailing punctuation. Keep the message short; put detail in
`extra`, not the string.

### Exception logging

Use `logger.exception()` only inside an `except` block you are not
re-raising from. Use `logger.error(..., exc_info=True)` when you need the
traceback outside an `except` block. Avoid `logger.exception()` followed by
`raise` — it duplicates the traceback; add context via `extra` instead, or
let the exception propagate.

### Avoid

f-strings or `.format()` in log calls; unguarded logging in hot loops;
catch-log-reraise with no new context; `print()` for diagnostics; logging a
secret env var's value (log the key name only); non-scalar ad-hoc objects in
`extra`; a custom `extra` field referenced in a format string with no safe
default (a missing key raises `KeyError`).

## Documented examples that run

Examples in this project are tests. This section is the contract for
writing one the test suite can actually see, and it states this repo's real
mechanism — read `[tool.pytest.ini_options]` in `pyproject.toml` before
assuming otherwise.

**A fence tag is cosmetic. Only a `>>> ` prompt executes.** A block written
as

    ```python
    parser = create_parser()
    ```

is prose that looks like a test. Nothing collects it, nothing runs it, and
it can be wrong for years. The same block written with prompts is a test:

    ```python
    >>> parser = create_parser()
    ```

This is the single most expensive mistake available when editing
documentation, because removing the prompts leaves a green test suite and a
silently deleted test. When editing a file that contains examples, count the
prompts before and after.

**The fence tag is `python`.** Not `pycon`, not bare.

**Where examples run, precisely.** `pyproject.toml` sets
`addopts = "--doctest-modules …"`, `doctest_optionflags = "ELLIPSIS
NORMALIZE_WHITESPACE"`, and `testpaths = ["src/g", "tests", "docs"]`.
Docstring examples under `src/g` run as part of every `pytest`/`py.test`
invocation. Markdown under `docs/` is also collected and executed — this was
verified directly: a `>>> ` prompt added to a page under `docs/` is
collected as its own test item and fails on a wrong expected value, exactly
like a docstring doctest. **`README.md` is not in `testpaths`.** A `>>> `
prompt there is never executed — there are none in the current README, and
adding one would silently do nothing rather than add a test, so do not
promise a reader that a README example is checked.

**No shared fixtures outside `src/g`.** This repository defines no
`doctest_namespace` fixture. A module doctest under `src/g` runs with that
module's own globals, so a name already imported or defined at module level
(`pathlib`, `create_parser`, `find_repo_type`, …) is available without
importing it again inside the block — see `create_parser`'s own docstring
for a working example. A prompted block anywhere else (`docs/`, if one is
ever added) starts bare: import or define every name the block uses.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing.

**Do not downgrade a doctest to a non-executed block to make it pass.** A
`.. code-block::` or an unprompted fence does not run. If an example cannot
pass, fix the example or fix the code.

**Option flags.** `ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled
globally, so `...` elides variable output and whitespace differences do not
fail a comparison. Reach for an inline `# doctest: +FLAG` only for the block
that needs it.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> parser = create_parser()
    >>> parser.prog
    'g'

**Console blocks are not examples that run.** A ```` ```console ```` block
at a `$` prompt is not collected by anything — `--doctest-modules` finds
doctests in Python modules, and the `docs/` collector runs `>>> ` blocks,
neither of which touches a shell transcript. Run a `console` block by hand
before committing it, and re-run it whenever you reshape the page around it;
nothing catches drift automatically.

## The changelog

`CHANGES` is the changelog, rendered as the Sphinx history page
(`docs/history.md`, published at `/history.html`). Its shape follows
Django's release-notes model —
deliverables get titles and prose, not bullets — because CHANGES here does
double duty as both the permanent ledger and the editorial release note;
there is no separate release page.

**Release entry boilerplate.** Every release header is
`## g X.Y.Z (YYYY-MM-DD)`. The file opens with a `## g X.Y.Z (unreleased)`
placeholder fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and
`<!-- END PLACEHOLDER ... -->` HTML comments — new entries land immediately
below the END marker, never above it.

**Open a release entry with a multi-sentence lead paragraph.** Plain prose,
no italics. Open with the version as the sentence subject ("g X.Y.Z
ships…") so the lead is self-contained when excerpted. Two to four
sentences on what shipped and who cares — user-visible takeaways, not
internal mechanism. Cross-reference detail docs with `{ref}` to keep the
lead compact.

**The unreleased entry carries no lead paragraph and no version summary** —
sections only (`### Breaking changes`, `### What's new` deliverables,
`### Fixes`, …). Speaking for a release — what the version "is", "ships", or
"focuses on" — is presumptuous before its scope is final. Only the person
cutting the release writes that, and only when the user explicitly asks to
release. Never write or edit a lead paragraph from a feature branch, and
never ask or imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`,
every distinct deliverable gets a `#### Deliverable title (#NN)` heading
naming it in user vocabulary, followed by one to three prose paragraphs. Do
not wrap a paragraph in `- ` — bullets are for enumerable lists, not
paragraph containers.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If you cannot answer in one sentence, the
entry is not ready. Mechanism — helper internals, byte counters,
schema-validation locations — belongs in the pull request description and
code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`,
`### Development`. Dev tooling (helper scripts, internal automation) lives
under `### Development`. For a breaking change, show the migration path
with a concrete `# Before` / `# After` code block. Dependency floor bumps
use ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items
use bullets — one line each, never paragraphs. A bullet that swells past two
lines gets promoted to a `#### Title (#NN)` heading with a prose body.

**Always link autodoc'd APIs** — any class, method, function, exception, or
attribute with its own rendered page — via the roles in
[Documentation cross-references](#documentation-cross-references), never
with plain backticks. Plain backticks stay correct for code syntax, env
vars, parameter names, and file paths that have no autodoc destination.

**Semantic-versioning meaning applies to the whole documented public
API** — command names, options, exit statuses, not only imported Python
symbols. A change to what `-V` prints or what a non-zero exit means is a
compatibility break here just as much as a signature change.

**Anti-patterns.** Fragile metrics that go stale silently — token
ceilings, third-party version pins, percent benchmarks, exact byte counts.
Describe the capability, not the math. Private symbols and internal jargon.
Walls of text dressed up as bullets. A breaking change buried mid-entry
instead of given its own subheading at the top.

**Summarization style.** Asked "what changed in the latest version?", lead
with the entry's lead paragraph (paraphrased if needed), then each `####`
deliverable heading under `### What's new` with a one-sentence summary. Cite
`(#NN)` only if asked for source links. Do not invent versions, dates, or
numbers absent from `CHANGES`; do not quote line numbers, which shift as the
file evolves.

## Docstrings

The prime directive: never restate the type. The annotation is the source of
truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def get_id(pane: Pane) -> str:
        """Get the pane's identifier.

        Parameters
        ----------
        pane : Pane
            The pane.

        Returns
        -------
        str
            The identifier.
        """

Document instead the dimensions the type system cannot encode: mutation,
ownership, ordering, timing, failure, idempotence, concurrency, units and
ranges, boundary behaviour, platform differences, and any security boundary
— what is executed versus what is only read.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an introspectable
signature.

Ruff's `pydocstyle` rule (`D`, `convention = "numpy"`) is the enforced
dialect — do not relitigate NumPy versus Google style in review.

**Classes with fields** — `NamedTuple`, dataclasses — document every field
in an `Attributes` section:

    class CommandLineTestFixture(t.NamedTuple):
        """Test fixture for CLI params, environment, and expected result.

        Attributes
        ----------
        test_id : str
            pytest parametrization id for the case.
        env : EnvFlag
            Directory state to simulate before invoking the CLI.
        argv_args : list[str]
            Arguments passed through to ``g`` on the command line.
        expect_cmd : str | None
            VCS command line expected, or ``None`` when none should run.
        """

Autodoc renders every field whether or not you describe it, so an
undocumented `NamedTuple` field ships to the API docs as "Alias for field
number 0", and a dataclass field ships bare. Document all of them — a class
with three fields and two documented still ships a stub for the third.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode the
code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and stop.
They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that hand-syncs
a value the code owns — a count, an offset, a line reference, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several facts,
in which case split it, or arguing, in which case cut it to the fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff, and
free to maintain.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency
  requirements that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not reintroduce
  the bug.
- A high-level sketch of an algorithm whose local operations do not reveal
  the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers — they say nothing to a reader without tracker
  access, and they rot when the tracker moves.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen
external facts.

Bad (Delete):

    # There are 321 tests to complete for servers.

Good (Keep):

    # CPython < 3.11 has no ExceptionGroup, so this branch stays.

### Documentation exception

Doctests, minimal usage examples, and `Parameters`/`Returns`/`Raises`
entries on public API are exempt from the loss gate — they serve the
caller, not the maintainer. They are exempt from nothing else. Ceiling: a
good man page entry.

## Terminology and capitalization

Pick the domain noun and keep it. Call the marker directories `.git`,
`.svn`, `.hg` and the thing they select the "VCS type" or "VCS command"
consistently, rather than alternating with "backend", "handler", or
"engine".

Python and PyPI keep their own capitalisation. Distribution names are
written as they are published.

Do not write counts into prose — how many tests exist, how many functions
are exported. They go stale silently and no reader needs them.

## Documentation cross-references

`docs/` is built with Sphinx and MyST. Class references use `{class}`,
methods `{meth}`, functions `{func}`, exceptions `{exc}`, attributes
`{attr}`, internal anchors `{ref}`, and doc-path links `{doc}`. A `{ref}`
must match its target's anchor exactly — anchors here are lowercase and
hyphenated (`cli-main`, `cli-supported-vcs`, `developmental-releases`).

Link the first prose mention of any symbol with a useful destination on
that page — a Python object, a CLI reference anchor, a project page, or an
external tool. Use the most specific role available for an API object;
`{ref}` or `{doc}` for a documentation page or section anchor; a plain
Markdown link for an external project. Do not rely on a later reference
section to satisfy the first-mention rule — if the first occurrence would
be a heading or a grid-card teaser, link that occurrence or retitle the
heading so the first prose mention can carry the link. Leave command
examples, code blocks, and literal values as code; link the surrounding
prose instead.

What stays exact, never paraphrased: the marker-to-command table, the
message strings named in [CLI and error messages](#cli-and-error-messages),
version strings, and function cross-references. Warm the framing sentences
around a precise block; never the block itself.

`make build_docs` catches a broken cross-reference; the test suite does
not — build the docs before committing a documentation change.
`docs/cli/index.md` is the worked example of all of the above: a
concept-first opening line, a three-step "How it works" before any
generated reference, and the precise marker table left exact below
everything the everyday reader needs.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue body
does not wrap at all: GitHub renders a single newline as a space in a file
and as a line break in a comment, so a wrapped comment body arrives as
ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Write the sentence so it carries the fact on its own, and a
renderer that drops the marker loses nothing.

Do not use a local absolute path or an email address in anything published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Executed examples are exempt — the test suite runs them,
nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments
  inside it.
- **Command menus are per-command blocks with prose lead-ins**, not tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware
  copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. Separate the `why:` and
`what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in `git log
--oneline`:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **ci**: Workflow and pipeline changes
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (`CLAUDE.md`)
- **ai(claude[command])**: Claude Code command changes

Example:

```
cli(feat[version]): Print version for -V

why: -V is the common short flag for version and was unhandled.

what:
- Treat -V as an alias for --version in run()
- Add a CLI test for the short flag
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The detailed
why and what go in the body. Do not use the `Scope(type[detail]):` format
for a release — it buries the lede.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file counts,
  dated "as of" claims, bare SHAs, or local absolute paths — unless they
  are strict evidentiary artefacts such as a benchmark log.
- **Diff narration.** Do not restate what moved, was renamed, or was
  removed in anything the reader holds alongside the diff: code,
  docstrings, README, or a pull request description. The diff and the
  commit message already carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of a
  published release actually experienced the old state.
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No
  `[R1]`, `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those
are the facts [Source comments](#source-comments) keeps, and every other
comment is judged by it.

### Durable source links

Link to a pinned revision, never to trunk, for anything cited as evidence.
`blob/master/…` links rot silently — the file moves, lines shift, and the
anchor lands on unrelated code while still resolving.

- Prefer a release tag (`blob/v1.4.0/…`). Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise use a 7-character commit SHA (`blob/9a29b1a/…`) reachable from
  trunk, for a claim about unreleased code. Never a pull-request-head SHA
  — it can be rebased or garbage-collected.
- Reserve `blob/master/…` for a living document meant to always show the
  latest state — `.github/CONTRIBUTING.md` and this file are exactly that
  case.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.
