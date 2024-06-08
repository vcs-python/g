#!/usr/bin/env python
"""Package for g."""

import io
import logging
import os
import pathlib
import subprocess
import sys
import typing as t
from os import PathLike

__all__ = ["DEFAULT", "run", "sys", "vcspath_registry"]

vcspath_registry = {".git": "git", ".svn": "svn", ".hg": "hg"}

log = logging.getLogger(__name__)


def find_repo_type(path: t.Union[pathlib.Path, str]) -> t.Optional[str]:
    """Detect repo type looking upwards."""
    for _path in [*list(pathlib.Path(path).parents), pathlib.Path(path)]:
        for p in _path.iterdir():
            if p.is_dir() and p.name in vcspath_registry:
                return vcspath_registry[p.name]
    return None


DEFAULT = object()


def run(
    cmd: t.Union[str, bytes, "PathLike[str]", "PathLike[bytes]", object] = DEFAULT,
    cmd_args: object = DEFAULT,
    wait: bool = False,
    *args: object,
    **kwargs: t.Any,
) -> t.Optional["subprocess.Popen[str]"]:
    """CLI Entrypoint for g, overlay for current directory's VCS utility.

    Environment variables
    ---------------------
    G_IS_TEST :
        Control whether run() returns proc so function can be tested. If proc was always
        returned, it would print *<Popen: returncode: 1 args: ['git']>* after command.
    """
    # Interpret default kwargs lazily for mockability of argv
    if cmd is DEFAULT:
        cmd = find_repo_type(pathlib.Path.cwd())
    if cmd_args is DEFAULT:
        cmd_args = sys.argv[1:]

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if cmd is None:
        msg = "No VCS found in current directory."
        log.info(msg)
        return None

    assert isinstance(cmd_args, (tuple, list))
    assert isinstance(cmd, (str, bytes, pathlib.Path))

    proc = subprocess.Popen([cmd, *cmd_args], **kwargs)
    if wait:
        proc.wait()
    else:
        proc.communicate()
    if os.getenv("G_IS_TEST") and __name__ != "__main__":
        return proc
    return None


if __name__ == "__main__":
    run()
