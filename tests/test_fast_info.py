"""Tests for the fast-info command."""

import json
from unittest.mock import patch


MOCK_FAST_INFO = {
    "currency": "USD",
    "lastPrice": 411.11,
    "lastVolume": 62559600,
    "open": 400.87,
    "previousClose": 397.21,
    "dayHigh": 414.55,
    "dayLow": 397.75,
    "yearHigh": 488.54,
    "yearLow": 138.80,
    "yearChange": 0.35,
    "marketCap": 1320000000000,
    "shares": 3210000000,
    "tenDayAverageVolume": 65000000,
    "threeMonthAverageVolume": 70000000,
    "fiftyDayAverage": 420.50,
    "twoHundredDayAverage": 380.25,
    "exchange": "NMS",
    "quoteType": "EQUITY",
    "timezone": "America/New_York",
}


@patch("src.commands.stock.yf.Ticker")
def test_fast_info_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
    code, data = invoke_json("fast-info", "TSLA")

    assert code == 0
    assert data["lastPrice"] == 411.11
    assert data["marketCap"] == 1320000000000
    assert data["exchange"] == "NMS"
    assert data["yearHigh"] == 488.54


@patch("src.commands.stock.yf.Ticker")
def test_fast_info_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_fast_info.return_value = None
    result = invoke("fast-info", "INVALID")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.stock.yf.Ticker")
def test_fast_info_ticker_uppercase(mock_ticker, invoke):
    mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
    invoke("fast-info", "tsla")
    mock_ticker.assert_called_once_with("TSLA")


@patch("src.commands.stock.yf.Ticker")
def test_fast_info_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_fast_info.side_effect = Exception("API Error")
    result = invoke("fast-info", "TSLA")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output


def test_fast_info_help(invoke):
    result = invoke("fast-info", "--help")
    assert result.exit_code == 0
    assert "TICKER" in result.output
