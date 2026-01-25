"""Tests for g's CLI package."""

from __future__ import annotations

import enum
import subprocess
import typing as t
from unittest.mock import patch

import pytest

from g import run

if t.TYPE_CHECKING:
    import pathlib


def get_output(
    *args: t.Any,
    **kwargs: t.Any,
) -> subprocess.CalledProcessError | t.Any:
    """Retrieve output from CLI subprocess, whether success or error."""
    try:
        return subprocess.check_output(*args, **kwargs)
    except subprocess.CalledProcessError as exc:
        return exc.output


class EnvFlag(enum.Enum):
    """Environmental conditions to simulate in test case."""

    Git = "Git"  # Inside a git directory (like this repo)
    Empty = "Empty"  # Empty directory (e.g. `tmp_path`)


@pytest.mark.parametrize(
    ("argv_args", "expect_cmd"),
    [
        (["g"], "git"),
        (["g", "--help"], "git --help"),
    ],
)
class CommandLineTestFixture(t.NamedTuple):
    """Test fixture for CLI params, environment, and expected result."""

    # pytest internal
    test_id: str

    # env data
    env: EnvFlag

    # test data
    argv_args: list[str]

    # results
    expect_cmd: str | None


TEST_FIXTURES: list[CommandLineTestFixture] = [
    CommandLineTestFixture(
        test_id="g-cmd-inside-git-dir",
        env=EnvFlag.Git,
        argv_args=["g"],
        expect_cmd="git",
    ),
    CommandLineTestFixture(
        test_id="g-cmd-help-inside-git-dir",
        env=EnvFlag.Git,
        argv_args=["g --help"],
        expect_cmd="git --help",
    ),
    CommandLineTestFixture(
        test_id="g-cmd-inside-empty-dir",
        env=EnvFlag.Empty,
        argv_args=["g"],
        expect_cmd=None,
    ),
    CommandLineTestFixture(
        test_id="g-cmd-help-inside-empty-dir",
        env=EnvFlag.Empty,
        argv_args=["g --help"],
        expect_cmd=None,
    ),
    CommandLineTestFixture(
        test_id="g-version-inside-git-dir",
        env=EnvFlag.Git,
        argv_args=["g", "--version"],
        expect_cmd=None,  # Returns None after printing version
    ),
    CommandLineTestFixture(
        test_id="g-version-short-inside-empty-dir",
        env=EnvFlag.Empty,
        argv_args=["g", "-V"],
        expect_cmd=None,
    ),
]


@pytest.mark.parametrize(
    list(CommandLineTestFixture._fields),
    TEST_FIXTURES,
    ids=[f.test_id for f in TEST_FIXTURES],
)
def test_command_line(
    # capsys: pytest.CaptureFixture[str],
    test_id: str,
    env: EnvFlag,
    argv_args: list[str],
    expect_cmd: str | None,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """Basic CLI usage."""
    from g import sys as gsys

    if env == EnvFlag.Git:
        pass
    elif env == EnvFlag.Empty:
        monkeypatch.chdir(str(tmp_path))

    with patch.object(gsys, "argv", argv_args):
        proc = run(wait=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if expect_cmd is None:
            assert proc is None
        else:
            assert proc is not None
            assert proc.stdout is not None
            captured = proc.stdout.read()

            assert captured == get_output(
                expect_cmd,
                shell=True,
                stderr=subprocess.STDOUT,
            )


def test_version_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --version prints the correct version string."""
    from g import __version__, sys as gsys

    with patch.object(gsys, "argv", ["g", "--version"]):
        result = run()
        assert result is None
        captured = capsys.readouterr()
        assert f"g {__version__}" in captured.out


def test_version_short_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that -V prints the correct version string."""
    from g import __version__, sys as gsys

    with patch.object(gsys, "argv", ["g", "-V"]):
        result = run()
        assert result is None
        captured = capsys.readouterr()
        assert f"g {__version__}" in captured.out
