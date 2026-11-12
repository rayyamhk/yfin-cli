"""Shared test fixtures for yfin-cli tests."""

import json
import os

# Typer forces colored output when GITHUB_ACTIONS (or FORCE_COLOR/PY_COLORS) is
# set, which injects ANSI codes into result.output and breaks text assertions in
# CI. Must be set before Typer's rich_utils is imported.
os.environ["_TYPER_FORCE_DISABLE_TERMINAL"] = "1"

import pytest  # noqa: E402
from typer.testing import CliRunner  # noqa: E402
from src.cli import app  # noqa: E402


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    """Mark every test that isn't `live` as `offline`, so `-m offline` selects them.

    tryfirst: must run before pytest applies the -m filter.
    """
    for item in items:
        if "live" not in item.keywords:
            item.add_marker(pytest.mark.offline)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def invoke(runner):
    """Invoke a CLI command and return the result."""

    def _invoke(*args):
        return runner.invoke(app, list(args))

    return _invoke


@pytest.fixture
def invoke_json(invoke):
    """Invoke a CLI command, parse JSON output, and return (exit_code, data)."""

    def _invoke_json(*args):
        result = invoke(*args)
        if result.exit_code != 0:
            return result.exit_code, result.output
        data = json.loads(result.output)
        return result.exit_code, data

    return _invoke_json
