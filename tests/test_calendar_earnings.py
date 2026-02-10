"""Tests for the earnings command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from src.cli import app

runner = CliRunner()


# Mock earnings data for testing
def create_mock_earnings_data():
    """Create a mock pandas DataFrame similar to yf.Calendars.get_earnings_calendar output."""
    data = {
        "Company": ["Test Corp", "Another Inc"],
        "Marketcap": [1000000000, 500000000],
        "Event Name": ["Q1 Earnings", "Q2 Earnings"],
        "Event Start Date": [
            pd.Timestamp("2026-02-10 13:30:00+0000"),
            pd.Timestamp("2026-02-11 21:00:00+0000"),
        ],
        "Timing": ["BMO", "AMC"],
        "EPS Estimate": [1.50, None],
        "Reported EPS": [None, None],
        "Surprise(%)": [None, None],
    }
    index = ["TEST", "ANOTHER"]
    return pd.DataFrame(data, index=index)


class TestEarningsCommand:
    """Tests for the calendar-earnings CLI command."""

    @patch("src.commands.calendar.yf.Calendars")
    def test_earnings_basic(self, mock_calendars):
        """Test basic calendar-earnings command execution."""
        mock_calendars.return_value.get_earnings_calendar.return_value = (
            create_mock_earnings_data()
        )
        result = runner.invoke(app, ["calendar-earnings"])
        assert result.exit_code == 0
        # Check for partial strings due to table wrapping
        assert "Test" in result.stdout
        assert "TEST" in result.stdout

    @patch("src.commands.calendar.yf.Calendars")
    def test_earnings_with_options(self, mock_calendars):
        """Test calendar-earnings command with options."""
        mock_calendars.return_value.get_earnings_calendar.return_value = (
            create_mock_earnings_data()
        )
        result = runner.invoke(
            app, ["calendar-earnings", "--limit", "5", "--start", "2026-02-01"]
        )
        assert result.exit_code == 0
        mock_calendars.return_value.get_earnings_calendar.assert_called_once()
        call_kwargs = mock_calendars.return_value.get_earnings_calendar.call_args[1]
        assert call_kwargs["limit"] == 5
        assert call_kwargs["start"] == "2026-02-01"

    @patch("src.commands.calendar.yf.Calendars")
    def test_earnings_no_data(self, mock_calendars):
        """Test calendar-earnings command when no data is found."""
        mock_calendars.return_value.get_earnings_calendar.return_value = pd.DataFrame()
        result = runner.invoke(app, ["calendar-earnings"])
        assert result.exit_code == 0
        assert "[]" in result.stdout

    def test_earnings_invalid_date(self):
        """Test calendar-earnings command with invalid date format."""
        result = runner.invoke(app, ["calendar-earnings", "--start", "invalid-date"])
        # Typer raises UsageError (exit code 2) for BadParameter.
        # Check result.output which captures both stdout and stderr.
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    @patch("src.commands.calendar.yf.Calendars")
    def test_earnings_api_error(self, mock_calendars):
        """Test calendar-earnings command handles API errors gracefully."""
        mock_calendars.return_value.get_earnings_calendar.side_effect = Exception(
            "API Error"
        )
        result = runner.invoke(app, ["calendar-earnings"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.stdout
