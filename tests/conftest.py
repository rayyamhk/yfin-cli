"""Shared test fixtures for yfin-cli tests."""

import json
import pytest
from typer.testing import CliRunner
from src.cli import app


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
