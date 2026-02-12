"""Tests for the calendar-earnings command."""

import pandas as pd
from unittest.mock import patch


def create_mock_earnings_data():
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


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_earnings_basic(mock_calendars, invoke_json):
    mock_calendars.return_value.get_earnings_calendar.return_value = (
        create_mock_earnings_data()
    )
    code, data = invoke_json("calendar-earnings")

    assert code == 0
    assert len(data) == 2
    assert data[0]["Company"] == "Test Corp"
    assert data[0]["Timing"] == "BMO"


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_earnings_with_options(mock_calendars, invoke_json):
    mock_calendars.return_value.get_earnings_calendar.return_value = (
        create_mock_earnings_data()
    )
    code, _ = invoke_json("calendar-earnings", "--limit", "5", "--start", "2026-02-01")

    assert code == 0
    call_kwargs = mock_calendars.return_value.get_earnings_calendar.call_args[1]
    assert call_kwargs["limit"] == 5
    assert call_kwargs["start"] == "2026-02-01"
    assert call_kwargs["end"] == "2026-02-08"


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_earnings_empty_data(mock_calendars, invoke_json):
    mock_calendars.return_value.get_earnings_calendar.return_value = pd.DataFrame()
    code, data = invoke_json("calendar-earnings")

    assert code == 0
    assert data == []


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_earnings_none_data(mock_calendars, invoke):
    mock_calendars.return_value.get_earnings_calendar.return_value = None
    result = invoke("calendar-earnings")

    assert result.exit_code == 1
    assert "No data found" in result.output


def test_calendar_earnings_invalid_date(invoke):
    result = invoke("calendar-earnings", "--start", "invalid-date")
    assert result.exit_code == 2
    assert "Invalid date format" in result.output


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_earnings_api_error(mock_calendars, invoke):
    mock_calendars.return_value.get_earnings_calendar.side_effect = Exception(
        "API Error"
    )
    result = invoke("calendar-earnings")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
