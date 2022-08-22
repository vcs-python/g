# `$ g`

Passthrough to your current directories vcs (or reach for it with --cwd)

[![Python Package](https://img.shields.io/pypi/v/g.svg)](https://pypi.org/project/g/)
[![Docs](https://github.com/vcs-python/g/workflows/docs/badge.svg)](https://g.git-pull.com)
[![Build Status](https://github.com/vcs-python/g/workflows/tests/badge.svg)](https://github.com/vcs-python/g/actions?query=workflow%3A%22tests%22)
[![Code Coverage](https://codecov.io/gh/vcs-python/g/branch/master/graph/badge.svg)](https://codecov.io/gh/vcs-python/g)
[![License](https://img.shields.io/github/license/vcs-python/g.svg)](https://github.com/vcs-python/g/blob/master/LICENSE)

Shortcut / powertool for developers to access current repos' vcs, whether it's
svn, hg, mercurial.

```console
$ pip install --user g
```

```console
$ g
```

### Developmental releases

You can test the unpublished version of g before its released.

- [pip](https://pip.pypa.io/en/stable/):

  ```console
  $ pip install --user --upgrade --pre g
  ```

- [pipx](https://pypa.github.io/pipx/docs/):

  ```console
  $ pipx install --suffix=@next g --pip-args '\--pre' --force
  ```

  Then use `g@next --help`.

# Credits

2021-12-05: Thanks to [John Shanahan](https://github.com/shanahanjrs) ([@\_shanahanjrs](https://twitter.com/_shanahanjrs)) for giving g use [g](https://pypi.org/project/g/)

# Donations

Your donations fund development of new features, testing and support.
Your money will go directly to maintenance and development of the
project. If you are an individual, feel free to give whatever feels
right for the value you get out of the project.

See donation options at <https://git-pull.com/support.html>.

# More information

- Python support: >= 3.7, pypy
- VCS supported: git(1), svn(1), hg(1)
- Source: <https://github.com/vcs-python/g>
- Docs: <https://g.git-pull.com>
- Changelog: <https://g.git-pull.com/history.html>
- API: <https://g.git-pull.com/api.html>
- Issues: <https://github.com/vcs-python/g/issues>
- Test Coverage: <https://codecov.io/gh/vcs-python/g>
- pypi: <https://pypi.python.org/pypi/g>
- Open Hub: <https://www.openhub.net/p/g>
- License: [MIT](https://opensource.org/licenses/MIT).
