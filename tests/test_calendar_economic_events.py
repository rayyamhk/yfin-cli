"""Tests for the calendar-economic-events command."""

import pandas as pd
from unittest.mock import patch


def create_mock_economic_data():
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


@patch("src.commands.calendar.yf.Calendars")
def test_economic_events_basic(mock_calendars, invoke_json):
    mock_calendars.return_value.get_economic_events_calendar.return_value = (
        create_mock_economic_data()
    )
    code, data = invoke_json("calendar-economic-events")

    assert code == 0
    assert len(data) == 2
    assert data[0]["Region"] == "US"
    assert data[0]["Actual"] == 2.5
    assert data[0]["Expected"] == 2.4


@patch("src.commands.calendar.yf.Calendars")
def test_economic_events_with_options(mock_calendars, invoke_json):
    mock_calendars.return_value.get_economic_events_calendar.return_value = (
        create_mock_economic_data()
    )
    code, _ = invoke_json(
        "calendar-economic-events", "--limit", "5", "--start", "2026-02-01"
    )

    assert code == 0
    call_kwargs = mock_calendars.return_value.get_economic_events_calendar.call_args[1]
    assert call_kwargs["limit"] == 5
    assert call_kwargs["start"] == "2026-02-01"
    assert call_kwargs["end"] == "2026-02-08"


@patch("src.commands.calendar.yf.Calendars")
def test_economic_events_empty_data(mock_calendars, invoke_json):
    mock_calendars.return_value.get_economic_events_calendar.return_value = (
        pd.DataFrame()
    )
    code, data = invoke_json("calendar-economic-events")

    assert code == 0
    assert data == []


@patch("src.commands.calendar.yf.Calendars")
def test_economic_events_none_data(mock_calendars, invoke):
    mock_calendars.return_value.get_economic_events_calendar.return_value = None
    result = invoke("calendar-economic-events")

    assert result.exit_code == 1
    assert "No data found" in result.output


def test_economic_events_invalid_date(invoke):
    result = invoke("calendar-economic-events", "--start", "invalid-date")
    assert result.exit_code == 2
    assert "Invalid date format" in result.output


@patch("src.commands.calendar.yf.Calendars")
def test_economic_events_api_error(mock_calendars, invoke):
    mock_calendars.return_value.get_economic_events_calendar.side_effect = Exception(
        "API Error"
    )
    result = invoke("calendar-economic-events")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
