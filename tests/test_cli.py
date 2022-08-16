import subprocess
import typing as t
from unittest.mock import patch

import pytest

from g import run


def get_output(
    *args: t.Any, **kwargs: t.Any
) -> t.Union[subprocess.CalledProcessError, t.Any]:
    try:
        result = subprocess.check_output(*args, **kwargs)
        return result
    except subprocess.CalledProcessError as exc:
        return exc.output


@pytest.mark.parametrize(
    "argv_args,expect_cmd",
    [
        (["g"], "git"),
        (["g", "--help"], "git --help"),
    ],
)
def test_command_line(
    # capsys: pytest.CaptureFixture[str],
    argv_args: t.List[str],
    expect_cmd: str,
) -> None:
    from g import sys as gsys

    with patch.object(gsys, "argv", argv_args):
        proc = run(wait=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc is not None
        assert proc.stdout is not None
        captured = proc.stdout.read()

        assert captured == get_output(expect_cmd, shell=True, stderr=subprocess.STDOUT)
