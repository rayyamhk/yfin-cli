"""Tests for the dividends command."""

import pandas as pd
from unittest.mock import patch


def create_mock_dividends_data():
    index = pd.DatetimeIndex(["2025-08-15", "2025-05-15", "2025-02-15", "2024-11-15"])
    return pd.Series([0.25, 0.25, 0.24, 0.24], index=index, name="Dividends")


@patch("src.commands.stock.yf.Ticker")
def test_dividends_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_dividends.return_value = create_mock_dividends_data()
    code, data = invoke_json("dividends", "AAPL")

    assert code == 0
    assert len(data) == 4
    assert data[0]["Dividends"] == 0.25


@patch("src.commands.stock.yf.Ticker")
def test_dividends_with_period(mock_ticker, invoke_json):
    mock_ticker.return_value.get_dividends.return_value = create_mock_dividends_data()
    code, _ = invoke_json("dividends", "AAPL", "--period", "1y")

    assert code == 0
    mock_ticker.return_value.get_dividends.assert_called_once_with(period="1y")


@patch("src.commands.stock.yf.Ticker")
def test_dividends_default_period(mock_ticker, invoke_json):
    mock_ticker.return_value.get_dividends.return_value = create_mock_dividends_data()
    invoke_json("dividends", "AAPL")
    mock_ticker.return_value.get_dividends.assert_called_once_with(period="max")


@patch("src.commands.stock.yf.Ticker")
def test_dividends_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.get_dividends.return_value = pd.Series(dtype=float)
    code, data = invoke_json("dividends", "AAPL")

    assert code == 0
    assert data == []


@patch("src.commands.stock.yf.Ticker")
def test_dividends_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_dividends.return_value = None
    result = invoke("dividends", "AAPL")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.stock.yf.Ticker")
def test_dividends_ticker_uppercase(mock_ticker, invoke):
    mock_ticker.return_value.get_dividends.return_value = create_mock_dividends_data()
    invoke("dividends", "aapl")
    mock_ticker.assert_called_once_with("AAPL")


def test_dividends_invalid_period(invoke):
    result = invoke("dividends", "AAPL", "--period", "invalid")
    assert result.exit_code == 2
    assert "Invalid" in result.output


@patch("src.commands.stock.yf.Ticker")
def test_dividends_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_dividends.side_effect = Exception("API Error")
    result = invoke("dividends", "AAPL")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
