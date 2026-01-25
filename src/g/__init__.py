#!/usr/bin/env python
"""Package for g."""

from __future__ import annotations

import argparse
import logging
import os
import pathlib
import subprocess
import sys
import typing as t
from os import PathLike

from g.__about__ import __version__

__all__ = ["DEFAULT", "create_parser", "run", "sys", "vcspath_registry"]

vcspath_registry = {".git": "git", ".svn": "svn", ".hg": "hg"}

log = logging.getLogger(__name__)


def find_repo_type(path: pathlib.Path | str) -> str | None:
    """Detect repo type looking upwards."""
    for _path in [*list(pathlib.Path(path).parents), pathlib.Path(path)]:
        for p in _path.iterdir():
            if p.is_dir() and p.name in vcspath_registry:
                return vcspath_registry[p.name]
    return None


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for g CLI.

    Returns
    -------
    argparse.ArgumentParser
        Configured argument parser for the g command.

    Examples
    --------
    >>> parser = create_parser()
    >>> parser.prog
    'g'

    >>> args = parser.parse_args(['status'])
    >>> args.vcs_args
    ['status']

    >>> args = parser.parse_args(['commit', '-m', 'message'])
    >>> args.vcs_args
    ['commit', '-m', 'message']
    """
    parser = argparse.ArgumentParser(
        prog="g",
        description="CLI alias for your current directory's VCS command (git, svn, hg).",
        epilog="All arguments are passed directly to the detected VCS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "vcs_args",
        nargs=argparse.REMAINDER,
        metavar="...",
        help="Arguments passed to the detected VCS (git, svn, or hg)",
    )
    return parser


DEFAULT = object()


def run(
    cmd: str | bytes | PathLike[str] | PathLike[bytes] | object = DEFAULT,
    cmd_args: object = DEFAULT,
    wait: bool = False,
    *args: object,
    **kwargs: t.Any,
) -> subprocess.Popen[str] | None:
    """CLI Entrypoint for g, overlay for current directory's VCS utility.

    Environment variables
    ---------------------
    G_IS_TEST :
        Control whether run() returns proc so function can be tested. If proc was always
        returned, it would print *<Popen: returncode: 1 args: ['git']>* after command.
    """
    # Interpret default kwargs lazily for mockability of argv
    if cmd_args is DEFAULT:
        cmd_args = sys.argv[1:]

    # Handle --version/-V before VCS detection
    assert isinstance(cmd_args, (tuple, list))
    if cmd_args and cmd_args[0] in ("--version", "-V"):
        parser = create_parser()
        parser.parse_args(["--version"])  # Will print version and exit

    if cmd is DEFAULT:
        cmd = find_repo_type(pathlib.Path.cwd())

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if cmd is None:
        msg = "No VCS found in current directory."
        log.info(msg)
        return None

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
