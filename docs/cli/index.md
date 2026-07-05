(cli)=

# CLI Reference

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} g
:link: cli-main
:link-type: ref
Proxy to your repo's VCS command.
:::

:::{grid-item-card} Supported VCS
:link: cli-supported-vcs
:link-type: ref
Repository detection.
:::

::::

g is a minimal CLI wrapper that proxies to your current directory's VCS command.
It detects [Git], [Subversion], and [Mercurial] repositories.

## How it works

When you run `g`, it:

1. Walks up from your current directory looking for `.git`, `.svn`, or `.hg`
2. Invokes the corresponding VCS (`git`, `svn`, or `hg`) with your arguments
3. Exits after the command completes

**Note:** `--version`/`-V` is handled by g itself rather than passed to the VCS.

## Usage examples

```console
$ g status
```

Is equivalent to:

In a git repo:

```console
$ git status
```

In an svn repo:

```console
$ svn status
```

In an hg repo:

```console
$ hg status
```

(cli-main)=

## Command

```{eval-rst}
.. argparse::
    :module: g
    :func: create_parser
    :prog: g
```

## Examples

```console
$ g status
```

```console
$ g commit -m "Fix bug"
```

```console
$ g log --oneline -10
```

```console
$ g diff HEAD~1
```

(cli-supported-vcs)=

## Supported VCS

| Directory marker | VCS command |
|------------------|-------------|
| `.git`           | `git`       |
| `.svn`           | `svn`       |
| `.hg`            | `hg`        |

[Git]: https://git-scm.com/
[Mercurial]: https://www.mercurial-scm.org/
[Subversion]: https://subversion.apache.org/
