"""Tests for the earnings-dates command."""

import pandas as pd
from unittest.mock import patch


def create_mock_earnings_dates_data():
    dates = [
        pd.Timestamp("2026-04-29 17:00:00-04:00"),
        pd.Timestamp("2026-01-28 16:00:00-05:00"),
        pd.Timestamp("2025-10-29 16:00:00-04:00"),
    ]
    data = {
        "EPS Estimate": [4.08, 3.85, 3.66],
        "Reported EPS": [None, 5.16, 3.72],
        "Surprise(%)": [None, 34.08, 1.59],
    }
    return pd.DataFrame(data, index=dates)


@patch("src.commands.financials.yf.Ticker")
def test_earnings_dates_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_earnings_dates.return_value = (
        create_mock_earnings_dates_data()
    )
    code, data = invoke_json("earnings-dates", "MSFT")

    assert code == 0
    assert len(data) == 3
    assert data[0]["EPS Estimate"] == 4.08
    assert data[1]["Reported EPS"] == 5.16
    assert data[1]["Surprise(%)"] == 34.08


@patch("src.commands.financials.yf.Ticker")
def test_earnings_dates_with_options(mock_ticker, invoke_json):
    mock_ticker.return_value.get_earnings_dates.return_value = (
        create_mock_earnings_dates_data()
    )
    code, _ = invoke_json("earnings-dates", "MSFT", "--limit", "5", "--offset", "10")

    assert code == 0
    mock_ticker.return_value.get_earnings_dates.assert_called_once_with(
        limit=5, offset=10
    )


@patch("src.commands.financials.yf.Ticker")
def test_earnings_dates_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.get_earnings_dates.return_value = pd.DataFrame()
    code, data = invoke_json("earnings-dates", "MSFT")

    assert code == 0
    assert data == []


@patch("src.commands.financials.yf.Ticker")
def test_earnings_dates_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_earnings_dates.return_value = None
    result = invoke("earnings-dates", "MSFT")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_earnings_dates_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_earnings_dates.side_effect = Exception("API Error")
    result = invoke("earnings-dates", "MSFT")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
