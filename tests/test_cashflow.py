"""Tests for the cashflow command."""

import pandas as pd
from unittest.mock import patch


def create_mock_cashflow_data(freq="yearly"):
    dates = [
        pd.Timestamp("2025-06-30"),
        pd.Timestamp("2024-06-30"),
        pd.Timestamp("2023-06-30"),
    ]
    if freq == "quarterly":
        dates = [
            pd.Timestamp("2025-06-30"),
            pd.Timestamp("2025-03-31"),
            pd.Timestamp("2024-12-31"),
        ]
    elif freq == "trailing":
        dates = [pd.NaT]

    data = {dates[0]: [5000.0, -2000.0]}
    if freq != "trailing":
        data[dates[1]] = [4000.0, -1500.0]
        data[dates[2]] = [3000.0, -1000.0]

    index = ["OperatingCashFlow", "CapitalExpenditure"]
    return pd.DataFrame(data, index=index)


@patch("src.commands.financials.yf.Ticker")
def test_cashflow_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_cashflow.return_value = create_mock_cashflow_data()
    code, data = invoke_json("cashflow", "MSFT")

    assert code == 0
    assert len(data) == 3
    assert data[0]["OperatingCashFlow"] == 5000.0
    assert data[0]["CapitalExpenditure"] == -2000.0
    mock_ticker.return_value.get_cashflow.assert_called_with(pretty=True, freq="yearly")


@patch("src.commands.financials.yf.Ticker")
def test_cashflow_quarterly(mock_ticker, invoke_json):
    mock_ticker.return_value.get_cashflow.return_value = create_mock_cashflow_data(
        "quarterly"
    )
    code, data = invoke_json("cashflow", "MSFT", "--frequency", "quarterly")

    assert code == 0
    assert "2025-03-31" in data[1]["Date"]
    mock_ticker.return_value.get_cashflow.assert_called_with(
        pretty=True, freq="quarterly"
    )


@patch("src.commands.financials.yf.Ticker")
def test_cashflow_trailing(mock_ticker, invoke_json):
    mock_ticker.return_value.get_cashflow.return_value = create_mock_cashflow_data(
        "trailing"
    )
    code, data = invoke_json("cashflow", "MSFT", "--frequency", "trailing")

    assert code == 0
    mock_ticker.return_value.get_cashflow.assert_called_with(
        pretty=True, freq="trailing"
    )


def test_cashflow_invalid_frequency(invoke):
    result = invoke("cashflow", "MSFT", "--frequency", "invalid")
    assert result.exit_code == 2
    assert "Invalid" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_cashflow_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.get_cashflow.return_value = pd.DataFrame()
    code, data = invoke_json("cashflow", "MSFT")

    assert code == 0
    assert data == []


@patch("src.commands.financials.yf.Ticker")
def test_cashflow_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_cashflow.return_value = None
    result = invoke("cashflow", "MSFT")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_cashflow_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_cashflow.side_effect = Exception("API Error")
    result = invoke("cashflow", "MSFT")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
