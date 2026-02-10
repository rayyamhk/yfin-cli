"""Tests for the sec-filings command."""

from unittest.mock import patch


MOCK_SEC_FILINGS = [
    {
        "date": "2025-10-30",
        "type": "10-K",
        "title": "Annual Report",
        "edgarUrl": "https://www.sec.gov/filing1",
    },
    {
        "date": "2025-07-31",
        "type": "10-Q",
        "title": "Quarterly Report",
        "edgarUrl": "https://www.sec.gov/filing2",
    },
]


@patch("src.commands.financials.yf.Ticker")
def test_sec_filings_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_sec_filings.return_value = MOCK_SEC_FILINGS
    code, data = invoke_json("sec-filings", "AAPL")

    assert code == 0
    assert len(data) == 2
    assert data[0]["type"] == "10-K"
    assert data[1]["type"] == "10-Q"


@patch("src.commands.financials.yf.Ticker")
def test_sec_filings_empty_data(mock_ticker, invoke_json):
    mock_ticker.return_value.get_sec_filings.return_value = []
    code, data = invoke_json("sec-filings", "AAPL")

    assert code == 0
    assert data == []


@patch("src.commands.financials.yf.Ticker")
def test_sec_filings_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_sec_filings.return_value = None
    result = invoke("sec-filings", "AAPL")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.financials.yf.Ticker")
def test_sec_filings_ticker_uppercase(mock_ticker, invoke):
    mock_ticker.return_value.get_sec_filings.return_value = MOCK_SEC_FILINGS
    invoke("sec-filings", "aapl")
    mock_ticker.assert_called_once_with("AAPL")


@patch("src.commands.financials.yf.Ticker")
def test_sec_filings_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_sec_filings.side_effect = Exception("API Error")
    result = invoke("sec-filings", "AAPL")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
