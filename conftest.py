"""Setup pytest for g."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def setup(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prepare pytest test environment.

    Environment variables
    ---------------------
    G_IS_TEST :
        Control whether run() returns proc so function can be tested. If proc was always
        returned, it would print *<Popen: returncode: 1 args: ['git']>* after command.
    """
    monkeypatch.setenv("G_IS_TEST", "1")
