#!/usr/bin/env python

import pathlib
import subprocess
import sys

vcspath_registry = {".git": "git", ".svn": "svn", ".hg": "hg"}


def find_repo_type(path):
    for path in list(pathlib.Path(path).parents) + [pathlib.Path(path)]:
        for p in path.iterdir():
            if p.is_dir():
                if p.name in vcspath_registry:
                    return vcspath_registry[p.name]


DEFAULT = object()


def run(cmd=DEFAULT, cmd_args=DEFAULT, *args, **kwargs):
    # Interpret default kwargs lazily for mockability of argv
    if cmd is DEFAULT:
        cmd = find_repo_type(pathlib.Path.cwd())
    if cmd_args is DEFAULT:
        cmd_args = sys.argv[1:]
    proc = subprocess.Popen([cmd, *cmd_args])
    proc.communicate()
    if __name__ != "__main__":
        return proc


if __name__ == "__main__":
    run()
