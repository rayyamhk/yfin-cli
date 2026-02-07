"""Tests for the calendar-economic-events command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from datetime import datetime
from src.cli import app
from src.commands.calendar_economic_events import _print_economic_events_table

runner = CliRunner()


# Mock Economic Events data for testing
def create_mock_economic_data():
    """Create a mock pandas DataFrame similar to yf.Calendars.get_economic_events_calendar output."""
    data = {
        "Region": ["US", "EU"],
        "Event Time": [
            pd.Timestamp("2026-02-14 13:30:00+0000"),
            pd.Timestamp("2026-02-15 10:00:00+0000"),
        ],
        "For": ["Jan", "Q4"],
        "Actual": [2.5, None],
        "Expected": [2.4, 1.2],
        "Last": [2.3, 1.1],
        "Revised": [None, 1.0],
    }
    index = ["CPI YoY", "GDP Growth"]
    return pd.DataFrame(data, index=index)


class TestEconomicEventsCommand:
    """Tests for the calendar-economic-events CLI command."""

    @patch("src.commands.calendar_economic_events.yf.Calendars")
    def test_economic_events_basic(self, mock_calendars):
        """Test basic calendar-economic-events command execution."""
        mock_calendars.return_value.get_economic_events_calendar.return_value = (
            create_mock_economic_data()
        )
        result = runner.invoke(app, ["calendar-economic-events"])
        assert result.exit_code == 0
        assert "CPI YoY" in result.output
        assert "US" in result.output

    @patch("src.commands.calendar_economic_events.yf.Calendars")
    def test_economic_events_with_options(self, mock_calendars):
        """Test calendar-economic-events command with options."""
        mock_calendars.return_value.get_economic_events_calendar.return_value = (
            create_mock_economic_data()
        )
        result = runner.invoke(
            app, ["calendar-economic-events", "--limit", "5", "--start", "2026-02-01"]
        )
        assert result.exit_code == 0
        mock_calendars.return_value.get_economic_events_calendar.assert_called_once()
        call_kwargs = (
            mock_calendars.return_value.get_economic_events_calendar.call_args[1]
        )
        assert call_kwargs["limit"] == 5
        assert call_kwargs["start"] == "2026-02-01"

    @patch("src.commands.calendar_economic_events.yf.Calendars")
    def test_economic_events_no_data(self, mock_calendars):
        """Test calendar-economic-events command when no data is found."""
        mock_calendars.return_value.get_economic_events_calendar.return_value = (
            pd.DataFrame()
        )
        result = runner.invoke(app, ["calendar-economic-events"])
        assert result.exit_code == 1
        assert "No economic events found" in result.output

    def test_economic_events_invalid_date(self):
        """Test calendar-economic-events command with invalid date format."""
        result = runner.invoke(
            app, ["calendar-economic-events", "--start", "invalid-date"]
        )
        # Typer raises UsageError (exit code 2) for BadParameter
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    @patch("src.commands.calendar_economic_events.yf.Calendars")
    def test_economic_events_api_error(self, mock_calendars):
        """Test calendar-economic-events command handles API errors gracefully."""
        mock_calendars.return_value.get_economic_events_calendar.side_effect = (
            Exception("API Error")
        )
        result = runner.invoke(app, ["calendar-economic-events"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output

    @patch("src.commands.calendar_economic_events.yf.Calendars")
    @patch("src.utils.datetime")
    def test_economic_events_default_dates(self, mock_datetime, mock_calendars):
        """Test calendar-economic-events command with no dates provided (defaults used)."""
        mock_calendars.return_value.get_economic_events_calendar.return_value = (
            create_mock_economic_data()
        )
        # Mock current date to a fixed point in time
        mock_now = datetime(2026, 2, 1)
        mock_datetime.now.return_value = mock_now

        # Ensure other datetime methods pass through correctly
        mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
        mock_datetime.strptime.side_effect = datetime.strptime

        result = runner.invoke(app, ["calendar-economic-events"])

        assert result.exit_code == 0
        call_kwargs = (
            mock_calendars.return_value.get_economic_events_calendar.call_args[1]
        )

        # Expected defaults: start=now, end=now+7
        expected_start = "2026-02-01"
        expected_end = "2026-02-08"

        assert call_kwargs["start"] == expected_start
        assert call_kwargs["end"] == expected_end


class TestPrintEconomicEventsTable:
    """Tests for the _print_economic_events_table helper function."""

    def test_print_economic_events_table_with_valid_data(self, capsys):
        """Test table printing with valid calendar-economic-events data."""
        # Patch console width to prevent wrapping
        from rich.console import Console

        with patch("src.utils.console", Console(width=200)):
            _print_economic_events_table(create_mock_economic_data())

        captured = capsys.readouterr()

        assert "CPI YoY" in captured.out
        assert "US" in captured.out
        # Actual value check
        assert "2.50" in captured.out
        # Expected value check
        assert "2.40" in captured.out
