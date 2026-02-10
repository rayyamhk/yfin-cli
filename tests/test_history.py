"""Tests for the history command."""

import json
import pandas as pd
import pytest
from unittest.mock import patch


def create_mock_history_data():
    data = {
        "Open": [100.0, 102.0],
        "High": [105.0, 108.0],
        "Low": [99.0, 101.0],
        "Close": [104.0, 107.0],
        "Volume": [1000000, 1200000],
    }
    index = pd.DatetimeIndex(["2026-02-05", "2026-02-06"])
    return pd.DataFrame(data, index=index)


@patch("src.commands.stock.yf.Ticker")
def test_history_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = create_mock_history_data()
    code, data = invoke_json("history", "AAPL")

    assert code == 0
    assert len(data) == 2
    assert data[0]["Close"] == 104.0
    assert data[1]["Volume"] == 1200000


@patch("src.commands.stock.yf.Ticker")
def test_history_with_interval(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = create_mock_history_data()
    code, _ = invoke_json("history", "TSLA", "--interval", "1h")

    assert code == 0
    call_kwargs = mock_ticker.return_value.history.call_args[1]
    assert call_kwargs["interval"] == "1h"


@patch("src.commands.stock.yf.Ticker")
def test_history_with_period(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = create_mock_history_data()
    code, _ = invoke_json("history", "TSLA", "--period", "5d")

    assert code == 0
    call_kwargs = mock_ticker.return_value.history.call_args[1]
    assert call_kwargs["period"] == "5d"


@patch("src.commands.stock.yf.Ticker")
def test_history_with_start_end(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = create_mock_history_data()
    code, _ = invoke_json("history", "TSLA", "--start", "2026-01-01", "--end", "2026-02-01")

    assert code == 0
    call_kwargs = mock_ticker.return_value.history.call_args[1]
    assert call_kwargs["start"] == "2026-01-01"
    assert call_kwargs["end"] == "2026-02-01"


@patch("src.commands.stock.yf.Ticker")
def test_history_default_period(mock_ticker, invoke_json):
    """Default period is 1mo when no time options specified."""
    mock_ticker.return_value.history.return_value = create_mock_history_data()
    invoke_json("history", "TSLA")

    call_kwargs = mock_ticker.return_value.history.call_args[1]
    assert call_kwargs["period"] == "1mo"


@pytest.mark.parametrize(
    "args, error_fragment",
    [
        (["--interval", "invalid"], "Invalid"),
        (["--period", "invalid"], "Invalid"),
        (["--start", "01-01-2026"], "Invalid date format"),
    ],
    ids=["invalid_interval", "invalid_period", "invalid_date"],
)
def test_history_invalid_input(invoke, args, error_fragment):
    result = invoke("history", "TSLA", *args)
    assert result.exit_code == 2
    assert error_fragment in result.output


def test_history_too_many_time_options(invoke):
    result = invoke(
        "history", "TSLA",
        "--period", "1mo",
        "--start", "2026-01-01",
        "--end", "2026-02-01",
    )
    assert result.exit_code != 0


@patch("src.commands.stock.yf.Ticker")
def test_history_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = pd.DataFrame()
    code, data = invoke_json("history", "TSLA")

    assert code == 0
    assert data == []


@patch("src.commands.stock.yf.Ticker")
def test_history_none_data(mock_ticker, invoke):
    mock_ticker.return_value.history.return_value = None
    result = invoke("history", "TSLA")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.stock.yf.Ticker")
def test_history_ticker_uppercase(mock_ticker, invoke):
    mock_ticker.return_value.history.return_value = create_mock_history_data()
    invoke("history", "tsla")
    mock_ticker.assert_called_once_with("TSLA")


@patch("src.commands.stock.yf.Ticker")
def test_history_api_error(mock_ticker, invoke):
    mock_ticker.return_value.history.side_effect = Exception("API Error")
    result = invoke("history", "TSLA")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
