(quickstart)=

# Quickstart

## Installation

For latest official version:

```console
$ pip install --user g
```

Upgrading:

```console
$ pip install --user --upgrade g
```

(developmental-releases)=

### Developmental releases

New versions of g are published to PyPI as alpha, beta, or release candidates.
In their versions you will see notification like `a1`, `b1`, and `rc1`, respectively.
`1.10.0b4` would mean the 4th beta release of `1.10.0` before general availability.

- [pip]\:

  ```console
  $ pip install --user --upgrade --pre g
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@next 'g' --pip-args '\--pre' --force
  ```

  Then use `g@next sync [config]...`.

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install --user -e git+https://github.com/vcs-python/g.git#egg=g
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@master 'g @ git+https://github.com/vcs-python/g.git@master' --force
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
