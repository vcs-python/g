(quickstart)=

# Quickstart

## Installation

For latest official version:

```console
$ pip install --user g
```

Or install with [uv](https://docs.astral.sh/uv/):

```console
$ uv tool install g
```

Add g to a uv-managed project:

```console
$ uv add g
```

Run g once without installing globally:

```console
$ uvx g
```

Upgrading:

```console
$ pip install --user --upgrade g
```

Or with uv:

```console
$ uv tool upgrade g
```

```console
$ uv add g
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

- [uv]\:

  ```console
  $ uv tool install g
  ```

  ```console
  $ uv add g
  ```

  ```console
  $ uvx g
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

- [uv]\:

  ```console
  $ uv tool install git+https://github.com/vcs-python/g.git
  ```

  ```console
  $ uv add git+https://github.com/vcs-python/g.git
  ```

  ```console
  $ uvx --from git+https://github.com/vcs-python/g.git g --version
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@master 'g @ git+https://github.com/vcs-python/g.git@master' --force
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[uv]: https://docs.astral.sh/uv/
