# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its mechanics. It complements
the repository-root `AGENTS.md`, which already governs doctests,
changelog conventions, MyST roles, and commit messages. When the two
overlap, the root file wins; this one only answers the question it
leaves open: how should the prose sound?

## Who you are writing for

The default reader works at a shell prompt inside a checkout and runs
`g` where they would type `git`, `svn`, or `hg`. They are fluent in
their own VCS — status, commit, log, diff — but you cannot assume they
read Python or know g's internals: `find_repo_type()`, the
`vcspath_registry` marker mapping, or the `G_IS_TEST` escape hatch the
tests use.

A second, smaller reader writes Python: they call `run()` directly,
build on `create_parser()`, or contribute to g itself. Serve them too,
but mark their material opt-in ("for the rarer cases", "internal") so
the default reader knows they can stop. Never make the common case pay
a comprehension tax for the advanced one.

## Voice

- **Second person, present tense, active.** "You run `g status`", not
  "The command is proxied". Address the reader who is doing the thing.
- **Concept before mechanics.** Open by saying what g *does* for the
  reader — one command that becomes the right VCS command. The
  generated option listing, the marker table, the exit behavior are
  the last details they need, not the first. A page that opens with
  argparse output has buried the idea under its plumbing.
- **Say when they can stop.** g has no configuration; most pages owe
  the reader one reassurance up front — run `g` where you'd run your
  VCS, and you're done. Let a skimmer leave after one sentence.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  everyday command → the one flag g intercepts (`--version`/`-V`) →
  how detection works → the Python entry points. Each step is for a
  smaller audience than the last.
- **Lean on the pipeline.** The reader's mental model is a straight
  line: current directory → walk up the parents → a `.git`, `.svn`,
  or `.hg` marker → the matching VCS command, with your arguments
  forwarded. Reinforce that chain when you explain detection or
  dispatch; it is the whole tool.
- **Name the trade-off.** If the thinness costs something, say so
  plainly: `--version`/`-V` never reaches the underlying VCS, and
  outside any repository g prints "No VCS found in current directory."
  and stops. State it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its directory marker or argparse detail in prose; that names the
  implementation surface, which is the reader's last concern. Name the
  concept — detection, forwarding. The mechanics vocabulary — the
  marker-to-command table, the generated option reference — belongs in
  the CLI reference, and only there.

## Keeping examples correct

Nothing executes the examples under `docs/` — `--doctest-modules`
runs the doctests in `src/g`'s docstrings, and `testpaths` includes
`docs/`, but Markdown prose is never collected. A ```` ```console ````
block is trusted as written, so it drifts silently. Run a command
before you commit it as an example, and when you reshape a page,
re-check that its examples still match what g prints today. Keep
shell examples in ```` ```console ```` blocks at a `$` prompt, one
command per block, as the existing pages do.

## What stays precise

Warm the framing, never the facts. The marker-to-command table, exact
message strings ("No VCS found in current directory."), version
strings, and function cross-references carry meaning in their exact
form — leave them alone. The friendly voice belongs in the sentences
*around* a precise block, introducing it, not inside it paraphrasing
it into vagueness.

## Cross-references

Point the curious reader at the deep-dive rather than inlining it, and
put the link where their interest peaks — on the phrase that made them
curious ("how detection works", "call it from Python") — not as a
standalone footnote the eye skips. Use the MyST roles listed in the
root `AGENTS.md` (`{func}`, `{class}`, `{meth}`, `{attr}`, `{exc}`,
`{ref}`, `{doc}`). A `{ref}` must match its target's anchor exactly —
anchors here are lowercase and hyphenated (`cli-main`,
`cli-supported-vcs`, `developmental-releases`). `make build_docs`
catches a broken cross-reference; the test suite does not — so build
the docs before you commit.

Link the first prose mention of any symbol that has a useful
destination on that page. This includes Python objects, g's API, CLI
reference anchors, project pages, and external tools or projects. Use
the most specific target available: `{func}`, `{class}`, `{meth}`,
`{mod}`, `{exc}`, or `{attr}` for API objects; `{ref}` or `{doc}` for
documentation pages and section anchors; and a Markdown link or
reference link for external projects. After the first linked mention
on a page, later mentions can stay plain unless the distance or
context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention
rule. If the first occurrence would be a heading, grid-card teaser, or
introductory sentence, link that occurrence or retitle the heading so
the first prose mention can carry the link. Leave command examples,
code blocks, and literal values as code; link the surrounding prose
instead.

## A page that does this

`docs/cli/index.md` is the worked example: a concept-first line — g
proxies to your current directory's VCS — a three-step "How it works"
before any generated reference, the `--version`/`-V` interception
stated plainly, everyday usage in ```` ```console ```` blocks, and the
precise directory-marker table left exact, below everything the
everyday reader needs. Read it before reshaping another page.

## Before you commit

- Does the page open with what g *does* for the reader, or with how
  the command line is parsed?
- Can a reader who only wants `g status` stop after the first
  paragraph?
- Is anything framed by its directory marker or argparse surface that
  should be named by concept instead?
- Are the Python-only and contributor parts clearly marked opt-in?
- Did you re-run any shell example you touched, and leave every table,
  message string, and cross-reference exact?
- Did `make build_docs` stay clean — no new warning, no broken
  cross-reference?
