"""Tests for the fast_info command."""

from typer.testing import CliRunner
from unittest.mock import patch
from src.cli import app

runner = CliRunner()


# Mock fast_info data for testing - must be dict-like to work with dict() call
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


class TestFastInfoCommand:
    """Tests for the fast-info CLI command."""

    @patch("src.commands.stock.yf.Ticker")
    def test_fast_info_basic(self, mock_ticker):
        """Test basic fast-info command execution."""
        mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
        result = runner.invoke(app, ["fast-info", "TSLA"])
        assert result.exit_code == 0
        assert "lastPrice" in result.output

    @patch("src.commands.stock.yf.Ticker")
    def test_fast_info_displays_metrics(self, mock_ticker):
        """Test that fast-info displays expected metrics."""
        mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
        result = runner.invoke(app, ["fast-info", "TSLA"])
        assert result.exit_code == 0
        assert "marketCap" in result.output
        assert "yearHigh" in result.output
        assert "exchange" in result.output

    @patch("src.commands.stock.yf.Ticker")
    def test_fast_info_no_data(self, mock_ticker):
        """Test fast-info command when no data is found."""
        mock_ticker.return_value.get_fast_info.return_value = None
        result = runner.invoke(app, ["fast-info", "INVALID"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output

    @patch("src.commands.stock.yf.Ticker")
    def test_fast_info_ticker_uppercase(self, mock_ticker):
        """Test that ticker is converted to uppercase."""
        mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
        runner.invoke(app, ["fast-info", "tsla"])
        mock_ticker.assert_called_once_with("TSLA")

    @patch("src.commands.stock.yf.Ticker")
    def test_fast_info_api_error(self, mock_ticker):
        """Test fast-info command handles API errors gracefully."""
        mock_ticker.return_value.get_fast_info.side_effect = Exception("API Error")
        result = runner.invoke(app, ["fast-info", "TSLA"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output


class TestHelpCommand:
    """Tests for the help output."""

    def test_fast_info_help(self):
        """Test fast-info --help shows correct info."""
        result = runner.invoke(app, ["fast-info", "--help"])
        assert result.exit_code == 0
        assert "TICKER" in result.output
        assert "fast info" in result.output.lower()
