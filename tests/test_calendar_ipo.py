"""Tests for the ipo command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from datetime import datetime
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

    @patch("src.commands.calendar_ipo.yf.Calendars")
    def test_ipo_basic(self, mock_calendars):
        """Test basic calendar_ipo command execution."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = (
            create_mock_ipo_data()
        )
        result = runner.invoke(app, ["calendar-ipo"])
        assert result.exit_code == 0
        assert "Tech" in result.output
        assert "TIPO" in result.output

    @patch("src.commands.calendar_ipo.yf.Calendars")
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

    @patch("src.commands.calendar_ipo.yf.Calendars")
    def test_ipo_no_data(self, mock_calendars):
        """Test calendar_ipo command when no data is found."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = pd.DataFrame()
        result = runner.invoke(app, ["calendar-ipo"])
        assert result.exit_code == 1
        assert "No IPOs found" in result.output

    def test_ipo_invalid_date(self):
        """Test calendar_ipo command with invalid date format."""
        result = runner.invoke(app, ["calendar-ipo", "--start", "invalid-date"])
        # Typer raises UsageError (exit code 2) for BadParameter
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    @patch("src.commands.calendar_ipo.yf.Calendars")
    def test_ipo_api_error(self, mock_calendars):
        """Test calendar_ipo command handles API errors gracefully."""
        mock_calendars.return_value.get_ipo_info_calendar.side_effect = Exception(
            "API Error"
        )
        result = runner.invoke(app, ["calendar-ipo"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output

    @patch("src.commands.calendar_ipo.yf.Calendars")
    def test_ipo_start_only(self, mock_calendars):
        """Test calendar_ipo command with start date only."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = (
            create_mock_ipo_data()
        )
        start_date = "2026-02-01"
        result = runner.invoke(app, ["calendar-ipo", "--start", start_date])

        assert result.exit_code == 0
        call_kwargs = mock_calendars.return_value.get_ipo_info_calendar.call_args[1]
        assert call_kwargs["start"] == start_date

        # End date should be start + 7 days
        expected_end = "2026-02-08"
        assert call_kwargs["end"] == expected_end

    @patch("src.commands.calendar_ipo.yf.Calendars")
    @patch("src.utils.datetime")
    def test_ipo_default_dates(self, mock_datetime, mock_calendars):
        """Test calendar_ipo command with no dates provided (defaults used)."""
        mock_calendars.return_value.get_ipo_info_calendar.return_value = (
            create_mock_ipo_data()
        )
        # Mock current date
        mock_now = datetime(2026, 2, 1)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
        mock_datetime.strptime.side_effect = datetime.strptime

        result = runner.invoke(app, ["calendar-ipo"])

        assert result.exit_code == 0
        call_kwargs = mock_calendars.return_value.get_ipo_info_calendar.call_args[1]

        expected_start = "2026-02-01"
        expected_end = "2026-02-08"

        assert call_kwargs["start"] == expected_start
        assert call_kwargs["end"] == expected_end
