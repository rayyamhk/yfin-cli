"""Tests for the income-stmt command."""

import pandas as pd
from unittest.mock import patch


def create_mock_income_data(freq="yearly"):
    dates = [
        pd.Timestamp("2025-09-30"),
        pd.Timestamp("2024-09-30"),
        pd.Timestamp("2023-09-30"),
    ]
    if freq == "quarterly":
        dates = [
            pd.Timestamp("2025-12-31"),
            pd.Timestamp("2025-09-30"),
            pd.Timestamp("2025-06-30"),
        ]

    data = {
        dates[0]: [1000.0, 500.0, 50.0],
        dates[1]: [900.0, 450.0, 45.0],
        dates[2]: [800.0, 400.0, 40.0],
    }
    index = ["TotalRevenue", "NetIncome", "EPS"]
    return pd.DataFrame(data, index=index)


@patch("src.commands.financials.yf.Ticker")
def test_income_stmt_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_income_stmt.return_value = create_mock_income_data()
    code, data = invoke_json("income-stmt", "AAPL")

    assert code == 0
    assert len(data) == 3
    assert data[0]["TotalRevenue"] == 1000.0
    assert data[0]["NetIncome"] == 500.0
    mock_ticker.return_value.get_income_stmt.assert_called_with(
        pretty=True, freq="yearly"
    )


@patch("src.commands.financials.yf.Ticker")
def test_income_stmt_quarterly(mock_ticker, invoke_json):
    mock_ticker.return_value.get_income_stmt.return_value = create_mock_income_data(
        "quarterly"
    )
    code, data = invoke_json("income-stmt", "AAPL", "--frequency", "quarterly")

    assert code == 0
    assert "2025-12-31" in data[0]["Date"]
    mock_ticker.return_value.get_income_stmt.assert_called_with(
        pretty=True, freq="quarterly"
    )


def test_income_stmt_invalid_frequency(invoke):
    result = invoke("income-stmt", "AAPL", "--frequency", "invalid")
    assert result.exit_code == 2
    assert "Invalid" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_income_stmt_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.get_income_stmt.return_value = pd.DataFrame()
    code, data = invoke_json("income-stmt", "AAPL")

    assert code == 0
    assert data == []


@patch("src.commands.financials.yf.Ticker")
def test_income_stmt_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_income_stmt.return_value = None
    result = invoke("income-stmt", "AAPL")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_income_stmt_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_income_stmt.side_effect = Exception("API Error")
    result = invoke("income-stmt", "AAPL")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
