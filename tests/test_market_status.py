"""Tests for the market-status command."""

from unittest.mock import patch


MOCK_MARKET_STATUS = {
    "market_state": "REGULAR",
    "exchange": "NMS",
    "timezone": "America/New_York",
}


@patch("src.commands.market.yf.Market")
def test_market_status_basic(mock_market, invoke_json):
    mock_market.return_value.status = MOCK_MARKET_STATUS
    code, data = invoke_json("market-status")

    assert code == 0
    assert data["market_state"] == "REGULAR"
    assert data["exchange"] == "NMS"


@patch("src.commands.market.yf.Market")
def test_market_status_none_data(mock_market, invoke):
    mock_market.return_value.status = None
    result = invoke("market-status")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.market.yf.Market")
def test_market_status_api_error(mock_market, invoke):
    mock_market.side_effect = Exception("API Error")
    result = invoke("market-status")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
