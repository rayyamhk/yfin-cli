"""Tests for error reporting: stderr only, JSON in JSON mode, exit codes, unknown tickers."""

import json
from unittest.mock import patch

import pandas as pd
import pytest


@pytest.fixture
def ticker_missing(monkeypatch):
    monkeypatch.setattr("src.decorators.ticker_exists", lambda ticker: False)


def _stderr_json(result):
    return json.loads(result.stderr)


@patch("src.commands.stock.yf.Ticker")
def test_unknown_ticker_with_empty_result_is_not_found(
    mock_ticker, invoke, ticker_missing
):
    mock_ticker.return_value.history.return_value = pd.DataFrame()
    result = invoke("history", "NOPE")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert _stderr_json(result) == {
        "error": "not_found",
        "message": "Ticker 'NOPE' not found on Yahoo Finance",
    }


@patch("src.commands.stock.yf.Ticker")
def test_unknown_ticker_with_all_null_result_is_not_found(
    mock_ticker, invoke, ticker_missing
):
    # `info` returns {"trailingPegRatio": None} for unknown symbols
    mock_ticker.return_value.get_info.return_value = {"trailingPegRatio": None}
    result = invoke("info", "NOPE")

    assert result.exit_code == 1
    assert _stderr_json(result)["error"] == "not_found"


@patch("src.commands.stock.yf.Ticker")
def test_unknown_ticker_that_raises_is_not_found(mock_ticker, invoke, ticker_missing):
    # `fast-info` raises KeyError('currency') for unknown symbols
    mock_ticker.return_value.fast_info.__getitem__.side_effect = KeyError("currency")
    mock_ticker.return_value.fast_info.keys.side_effect = KeyError("currency")
    result = invoke("fast-info", "NOPE")

    assert result.exit_code == 1
    assert _stderr_json(result)["error"] == "not_found"


@patch("src.commands.stock.yf.Ticker")
def test_valid_ticker_with_empty_result_returns_empty_list(mock_ticker, invoke):
    mock_ticker.return_value.history.return_value = pd.DataFrame()
    result = invoke("history", "SPY")

    assert result.exit_code == 0
    assert json.loads(result.stdout) == []
    assert result.stderr == ""


@patch("src.commands.stock.yf.Ticker")
def test_unexpected_error_goes_to_stderr_as_json(mock_ticker, invoke):
    mock_ticker.return_value.history.side_effect = RuntimeError("boom")
    result = invoke("history", "AAPL")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert _stderr_json(result) == {
        "error": "error",
        "message": "Unexpected error: boom",
    }


@patch("src.commands.stock.yf.Ticker")
def test_errors_are_plain_text_in_table_mode(mock_ticker, invoke, ticker_missing):
    mock_ticker.return_value.history.return_value = pd.DataFrame()
    result = invoke("--output", "table", "history", "NOPE")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "Ticker 'NOPE' not found" in result.stderr


@patch("src.commands.sector.yf.Sector")
def test_bad_sector_key_points_to_sector_keys(mock_sector, invoke):
    mock_sector.return_value.overview = None
    result = invoke("sector-overview", "not-a-sector")

    assert result.exit_code == 1
    error = _stderr_json(result)
    assert error["error"] == "no_data"
    assert "yfin sector-keys" in error["message"]
