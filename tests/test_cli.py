import subprocess
from unittest.mock import patch

import pytest

from g import run


def get_output(*args, **kwargs):
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
def test_command_line(capsys, argv_args, expect_cmd):
    from g import sys as gsys

    with patch.object(gsys, "argv", argv_args):
        run(stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)
        captured = capsys.readouterr().out
    with capsys.disabled():
        assert captured == get_output(expect_cmd, shell=True, stderr=subprocess.STDOUT)
