"""Tests for the ipo command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from src.cli import app

runner = CliRunner()


# Mock IPO data for testing
def create_mock_ipo_data():
    """Create a mock pandas DataFrame similar to yf.Calendars.get_ipo_info_calendar output."""
    data = {
        "Company": ["Tech IPO Inc", "BioTech Ltd"],
        "Exchange": ["NASDAQ", "NYSE"],
        "Date": [
            pd.Timestamp("2026-02-15 09:30:00+0000"),
            pd.Timestamp("2026-02-16 09:30:00+0000"),
        ],
        "Price From": [10.0, 20.0],
        "Price To": [12.0, 22.0],
        "Price": [None, 21.0],
        "Currency": ["USD", "USD"],
        "Shares": [1000000, 500000],
        "Action": ["Expected", "Priced"],
    }
    index = ["TIPO", "BIO"]
    return pd.DataFrame(data, index=index)


class TestIPOCommand:
    """Tests for the ipo CLI command."""

    @patch("src.commands.calendar.yf.Calendars")
    def test_ipo_basic(self, mock_calendars):
        """Test basic calendar_ipo command execution."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = (
            create_mock_ipo_data()
        )
        result = runner.invoke(app, ["calendar-ipo"])
        assert result.exit_code == 0
        assert "Tech" in result.output
        assert "TIPO" in result.output

    @patch("src.commands.calendar.yf.Calendars")
    def test_ipo_with_options(self, mock_calendars):
        """Test calendar_ipo command with options."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = (
            create_mock_ipo_data()
        )
        result = runner.invoke(
            app, ["calendar-ipo", "--limit", "5", "--start", "2026-02-01"]
        )
        assert result.exit_code == 0
        mock_calendars.return_value.get_ipo_info_calendar.assert_called_once()
        call_kwargs = mock_calendars.return_value.get_ipo_info_calendar.call_args[1]
        assert call_kwargs["limit"] == 5
        assert call_kwargs["start"] == "2026-02-01"

    @patch("src.commands.calendar.yf.Calendars")
    def test_ipo_no_data(self, mock_calendars):
        """Test calendar_ipo command when no data is found."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = pd.DataFrame()
        result = runner.invoke(app, ["calendar-ipo"])
        assert result.exit_code == 0
        assert "[]" in result.output

    def test_ipo_invalid_date(self):
        """Test calendar_ipo command with invalid date format."""
        result = runner.invoke(app, ["calendar-ipo", "--start", "invalid-date"])
        # Typer raises UsageError (exit code 2) for BadParameter
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    @patch("src.commands.calendar.yf.Calendars")
    def test_ipo_api_error(self, mock_calendars):
        """Test calendar_ipo command handles API errors gracefully."""
        mock_calendars.return_value.get_ipo_info_calendar.side_effect = Exception(
            "API Error"
        )
        result = runner.invoke(app, ["calendar-ipo"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output
