"""Tests for the earnings-dates command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from src.cli import app

runner = CliRunner()


# Mock Earnings Dates data for testing
def create_mock_earnings_dates_data():
    """Create a mock pandas DataFrame similar to yf.Ticker.get_earnings_dates output."""
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


class TestEarningsDatesCommand:
    """Tests for the earnings-dates CLI command."""

    @patch("src.commands.financials.yf.Ticker")
    def test_earnings_dates_basic(self, mock_ticker):
        """Test basic earnings-dates command execution."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_earnings_dates.return_value = (
            create_mock_earnings_dates_data()
        )

        result = runner.invoke(app, ["earnings-dates", "MSFT"])

        assert result.exit_code == 0
        assert "2026-04-29" in result.output
        assert "4.08" in result.output
        assert "34.08" in result.output  # Raw percent value

        # Verify call args
        mock_instance.get_earnings_dates.assert_called_once()

    @patch("src.commands.financials.yf.Ticker")
    def test_earnings_dates_no_data(self, mock_ticker):
        """Test earnings-dates command when no data is found."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_earnings_dates.return_value = pd.DataFrame()

        result = runner.invoke(app, ["earnings-dates", "MSFT"])

        # Typer exit code 1 raised explicitly
        assert result.exit_code == 1
        assert "No data found" in result.output

    @patch("src.commands.financials.yf.Ticker")
    def test_earnings_dates_none_data(self, mock_ticker):
        """Test earnings-dates command when data is None."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_earnings_dates.return_value = None

        result = runner.invoke(app, ["earnings-dates", "MSFT"])

        assert result.exit_code == 1
        assert "No data found" in result.output

    @patch("src.commands.financials.yf.Ticker")
    def test_earnings_dates_api_error(self, mock_ticker):
        """Test earnings-dates command handles API errors."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_earnings_dates.side_effect = Exception("API Error")

        result = runner.invoke(app, ["earnings-dates", "MSFT"])

        assert result.exit_code == 1
        assert "Unexpected error" in result.output
