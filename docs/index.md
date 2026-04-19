(index)=

# g

A tiny CLI wrapper for git, svn, and hg -- auto-detects your repo type and proxies commands.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install and run your first command.
:::

:::{grid-item-card} CLI Reference
:link: cli/index
:link-type: doc
Every command, flag, and option.
:::

:::{grid-item-card} Contributing
:link: project/index
:link-type: doc
Development setup, code style, and releases.
:::

::::

## Install

```console
$ pip install --user g
```

```console
$ uv tool install g
```

See [Quickstart](quickstart.md) for all installation methods and first steps.

## At a glance

```console
$ g status
```

Inside a git repo this runs `git status`; inside an svn checkout it runs `svn status`; inside a mercurial repo it runs `hg status`.

```{toctree}
:hidden:

quickstart
cli/index
api
project/index
history
GitHub <https://github.com/vcs-python/g>
```
