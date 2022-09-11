#!/usr/bin/env python
import pathlib
import subprocess
import sys
import typing as t
from os import PathLike

__all__ = ["sys", "vcspath_registry", "DEFAULT", "run"]

vcspath_registry = {".git": "git", ".svn": "svn", ".hg": "hg"}


def find_repo_type(path: t.Union[pathlib.Path, str]) -> t.Optional[str]:
    for path in list(pathlib.Path(path).parents) + [pathlib.Path(path)]:
        for p in path.iterdir():
            if p.is_dir():
                if p.name in vcspath_registry:
                    return vcspath_registry[p.name]
    return None


DEFAULT = object()


def run(
    cmd: t.Union[str, bytes, "PathLike[str]", "PathLike[bytes]", object] = DEFAULT,
    cmd_args: object = DEFAULT,
    wait: bool = False,
    *args: object,
    **kwargs: t.Any
) -> t.Optional["subprocess.Popen[str]"]:
    # Interpret default kwargs lazily for mockability of argv
    if cmd is DEFAULT:
        cmd = find_repo_type(pathlib.Path.cwd())
    if cmd_args is DEFAULT:
        cmd_args = sys.argv[1:]

    assert isinstance(cmd_args, (tuple, list))
    assert isinstance(cmd, (str, bytes, pathlib.Path))

    proc = subprocess.Popen([cmd, *cmd_args], **kwargs)
    if wait:
        proc.wait()
    else:
        proc.communicate()
    if __name__ != "__main__":
        return proc
    return None


if __name__ == "__main__":
    run()
