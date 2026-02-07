"""Tests for the fast_info command."""

from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from src.cli import app
from src.commands.fast_info import _print_fast_info_table

runner = CliRunner()


# Mock fast_info data for testing
MOCK_FAST_INFO = MagicMock()
MOCK_FAST_INFO.get.side_effect = lambda key: {
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
}.get(key)


class TestFastInfoCommand:
    """Tests for the fast-info CLI command."""

    @patch("src.commands.fast_info.yf.Ticker")
    def test_fast_info_basic(self, mock_ticker):
        """Test basic fast-info command execution."""
        mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
        result = runner.invoke(app, ["fast-info", "TSLA"])
        assert result.exit_code == 0
        assert "Last Price" in result.stdout

    @patch("src.commands.fast_info.yf.Ticker")
    def test_fast_info_displays_metrics(self, mock_ticker):
        """Test that fast-info displays expected metrics."""
        mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
        result = runner.invoke(app, ["fast-info", "TSLA"])
        assert result.exit_code == 0
        assert "Market Cap" in result.stdout
        assert "52-Week High" in result.stdout
        assert "Exchange" in result.stdout

    @patch("src.commands.fast_info.yf.Ticker")
    def test_fast_info_no_data(self, mock_ticker):
        """Test fast-info command when no data is found."""
        mock_ticker.return_value.get_fast_info.return_value = None
        result = runner.invoke(app, ["fast-info", "INVALID"])
        assert result.exit_code == 1
        assert "No info found" in result.stdout

    @patch("src.commands.fast_info.yf.Ticker")
    def test_fast_info_ticker_uppercase(self, mock_ticker):
        """Test that ticker is converted to uppercase."""
        mock_ticker.return_value.get_fast_info.return_value = MOCK_FAST_INFO
        runner.invoke(app, ["fast-info", "tsla"])
        mock_ticker.assert_called_once_with("TSLA")

    @patch("src.commands.fast_info.yf.Ticker")
    def test_fast_info_api_error(self, mock_ticker):
        """Test fast-info command handles API errors gracefully."""
        mock_ticker.return_value.get_fast_info.side_effect = Exception("API Error")
        result = runner.invoke(app, ["fast-info", "TSLA"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.stdout


class TestPrintFastInfoTable:
    """Tests for the _print_fast_info_table helper function."""

    def test_print_fast_info_table_with_valid_data(self, capsys):
        """Test table printing with valid fast info data."""
        _print_fast_info_table("TSLA", MOCK_FAST_INFO)
        captured = capsys.readouterr()
        assert "Last Price" in captured.out
        assert "Market Cap" in captured.out

    def test_print_fast_info_table_with_missing_fields(self, capsys):
        """Test table handles missing fields gracefully."""
        empty_info = MagicMock()
        empty_info.get.return_value = None
        _print_fast_info_table("TSLA", empty_info)
        captured = capsys.readouterr()
        assert "N/A" in captured.out

    def test_print_fast_info_table_formats_market_cap(self, capsys):
        """Test that market cap is formatted correctly."""
        trillion_info = MagicMock()
        trillion_info.get.side_effect = lambda key: {
            "marketCap": 2500000000000,  # 2.5T
        }.get(key)
        _print_fast_info_table("AAPL", trillion_info)
        captured = capsys.readouterr()
        assert "$2.50T" in captured.out


class TestHelpCommand:
    """Tests for the help output."""

    def test_fast_info_help(self):
        """Test fast-info --help shows correct info."""
        result = runner.invoke(app, ["fast-info", "--help"])
        assert result.exit_code == 0
        assert "TICKER" in result.stdout
        assert "fast info" in result.stdout.lower()
