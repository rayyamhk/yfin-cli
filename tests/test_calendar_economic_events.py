"""Tests for the calendar-economic-events command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from src.cli import app

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

    @patch("src.commands.calendar.yf.Calendars")
    def test_economic_events_basic(self, mock_calendars):
        """Test basic calendar-economic-events command execution."""
        mock_calendars.return_value.get_economic_events_calendar.return_value = (
            create_mock_economic_data()
        )
        result = runner.invoke(app, ["calendar-economic-events"])
        assert result.exit_code == 0
        assert "CPI YoY" in result.output
        assert "US" in result.output

    @patch("src.commands.calendar.yf.Calendars")
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

    @patch("src.commands.calendar.yf.Calendars")
    def test_economic_events_no_data(self, mock_calendars):
        """Test calendar-economic-events command when no data is found."""
        mock_calendars.return_value.get_economic_events_calendar.return_value = (
            pd.DataFrame()
        )
        result = runner.invoke(app, ["calendar-economic-events"])
        assert result.exit_code == 1
        assert "No data found" in result.output

    def test_economic_events_invalid_date(self):
        """Test calendar-economic-events command with invalid date format."""
        result = runner.invoke(
            app, ["calendar-economic-events", "--start", "invalid-date"]
        )
        # Typer raises UsageError (exit code 2) for BadParameter
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    @patch("src.commands.calendar.yf.Calendars")
    def test_economic_events_api_error(self, mock_calendars):
        """Test calendar-economic-events command handles API errors gracefully."""
        mock_calendars.return_value.get_economic_events_calendar.side_effect = (
            Exception("API Error")
        )
        result = runner.invoke(app, ["calendar-economic-events"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output
