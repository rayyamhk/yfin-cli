"""Tests for the earnings command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from datetime import datetime
from src.cli import app
from src.commands.calendar_earnings import _print_earnings_table

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

    @patch("src.commands.calendar_earnings.yf.Calendars")
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

    @patch("src.commands.calendar_earnings.yf.Calendars")
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

    @patch("src.commands.calendar_earnings.yf.Calendars")
    def test_earnings_no_data(self, mock_calendars):
        """Test calendar-earnings command when no data is found."""
        mock_calendars.return_value.get_earnings_calendar.return_value = pd.DataFrame()
        result = runner.invoke(app, ["calendar-earnings"])
        assert result.exit_code == 1
        assert "No earnings found" in result.stdout

    def test_earnings_invalid_date(self):
        """Test calendar-earnings command with invalid date format."""
        result = runner.invoke(app, ["calendar-earnings", "--start", "invalid-date"])
        # Typer raises UsageError (exit code 2) for BadParameter.
        # Check result.output which captures both stdout and stderr.
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    @patch("src.commands.calendar_earnings.yf.Calendars")
    def test_earnings_api_error(self, mock_calendars):
        """Test calendar-earnings command handles API errors gracefully."""
        mock_calendars.return_value.get_earnings_calendar.side_effect = Exception(
            "API Error"
        )
        result = runner.invoke(app, ["calendar-earnings"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.stdout

    @patch("src.commands.calendar_earnings.yf.Calendars")
    def test_earnings_start_only(self, mock_calendars):
        """Test calendar-earnings command with start date only (end date calculated)."""
        mock_calendars.return_value.get_earnings_calendar.return_value = (
            create_mock_earnings_data()
        )
        start_date = "2026-02-01"
        result = runner.invoke(app, ["calendar-earnings", "--start", start_date])

        assert result.exit_code == 0
        call_kwargs = mock_calendars.return_value.get_earnings_calendar.call_args[1]
        assert call_kwargs["start"] == start_date

        # End date should be start + 7 days
        expected_end = "2026-02-08"
        assert call_kwargs["end"] == expected_end

    @patch("src.commands.calendar_earnings.yf.Calendars")
    def test_earnings_end_only(self, mock_calendars):
        """Test calendar-earnings command with end date only (start date calculated)."""
        mock_calendars.return_value.get_earnings_calendar.return_value = (
            create_mock_earnings_data()
        )
        end_date = "2026-02-08"
        result = runner.invoke(app, ["calendar-earnings", "--end", end_date])

        assert result.exit_code == 0
        call_kwargs = mock_calendars.return_value.get_earnings_calendar.call_args[1]
        assert call_kwargs["end"] == end_date

        # Start date should be end - 7 days
        expected_start = "2026-02-01"
        assert call_kwargs["start"] == expected_start

    @patch("src.commands.calendar_earnings.yf.Calendars")
    def test_earnings_start_and_end(self, mock_calendars):
        """Test calendar-earnings command with both start and end dates."""
        mock_calendars.return_value.get_earnings_calendar.return_value = (
            create_mock_earnings_data()
        )
        start_date = "2026-02-01"
        end_date = "2026-02-05"
        result = runner.invoke(
            app, ["calendar-earnings", "--start", start_date, "--end", end_date]
        )

        assert result.exit_code == 0
        call_kwargs = mock_calendars.return_value.get_earnings_calendar.call_args[1]
        assert call_kwargs["start"] == start_date
        assert call_kwargs["end"] == end_date

    def test_earnings_invalid_range(self):
        """Test calendar-earnings command where start date is after end date."""
        result = runner.invoke(
            app, ["calendar-earnings", "--start", "2026-02-10", "--end", "2026-02-01"]
        )
        assert result.exit_code == 1
        assert "Start date must be before end date" in result.stdout

    @patch("src.commands.calendar_earnings.yf.Calendars")
    @patch("src.utils.datetime")
    def test_earnings_default_dates(self, mock_datetime, mock_calendars):
        """Test calendar-earnings command with no dates provided (defaults used)."""
        mock_calendars.return_value.get_earnings_calendar.return_value = (
            create_mock_earnings_data()
        )
        # Mock current date to a fixed point in time
        mock_now = datetime(2026, 2, 1)
        mock_datetime.now.return_value = mock_now

        # Ensure other datetime methods pass through correctly
        mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
        mock_datetime.strptime.side_effect = datetime.strptime

        result = runner.invoke(app, ["calendar-earnings"])

        assert result.exit_code == 0
        call_kwargs = mock_calendars.return_value.get_earnings_calendar.call_args[1]

        # Expected defaults: start=now, end=now+7
        expected_start = "2026-02-01"
        expected_end = "2026-02-08"

        assert call_kwargs["start"] == expected_start
        assert call_kwargs["end"] == expected_end


class TestPrintEarningsTable:
    """Tests for the _print_earnings_table helper function."""

    def test_print_earnings_table_with_valid_data(self, capsys):
        """Test table printing with valid earnings data."""
        _print_earnings_table(create_mock_earnings_data())
        captured = capsys.readouterr()
        # Check for key portions of data
        assert "Test" in captured.out
        assert "1.50" in captured.out
        assert "BMO" in captured.out

    def test_print_earnings_table_with_nan_eps(self, capsys):
        """Test table handles NaN EPS gracefully."""
        data = create_mock_earnings_data()
        # The second row has None EPS in our mock data creator
        _print_earnings_table(data)
        captured = capsys.readouterr()
        # Check for truncated company name due to table wrapping
        assert "Anoth" in captured.out
