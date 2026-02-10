"""Tests for the balance-sheet command."""

import pandas as pd
from unittest.mock import patch


def create_mock_balance_sheet_data(freq="yearly"):
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

    data = {
        dates[0]: [10000.0, 5000.0],
        dates[1]: [9000.0, 4500.0],
        dates[2]: [8000.0, 4000.0],
    }
    index = ["TotalAssets", "TotalLiabilities"]
    return pd.DataFrame(data, index=index)


@patch("src.commands.financials.yf.Ticker")
def test_balance_sheet_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_balance_sheet.return_value = (
        create_mock_balance_sheet_data()
    )
    code, data = invoke_json("balance-sheet", "MSFT")

    assert code == 0
    assert len(data) == 3
    assert data[0]["TotalAssets"] == 10000.0
    assert data[0]["TotalLiabilities"] == 5000.0
    mock_ticker.return_value.get_balance_sheet.assert_called_with(
        pretty=True, freq="yearly"
    )


@patch("src.commands.financials.yf.Ticker")
def test_balance_sheet_quarterly(mock_ticker, invoke_json):
    mock_ticker.return_value.get_balance_sheet.return_value = (
        create_mock_balance_sheet_data("quarterly")
    )
    code, data = invoke_json("balance-sheet", "MSFT", "--frequency", "quarterly")

    assert code == 0
    assert "2025-03-31" in data[1]["Date"]
    mock_ticker.return_value.get_balance_sheet.assert_called_with(
        pretty=True, freq="quarterly"
    )


def test_balance_sheet_invalid_frequency(invoke):
    result = invoke("balance-sheet", "MSFT", "--frequency", "invalid")
    assert result.exit_code == 2
    assert "Invalid" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_balance_sheet_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.get_balance_sheet.return_value = pd.DataFrame()
    code, data = invoke_json("balance-sheet", "MSFT")

    assert code == 0
    assert data == []


@patch("src.commands.financials.yf.Ticker")
def test_balance_sheet_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_balance_sheet.return_value = None
    result = invoke("balance-sheet", "MSFT")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_balance_sheet_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_balance_sheet.side_effect = Exception("API Error")
    result = invoke("balance-sheet", "MSFT")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
