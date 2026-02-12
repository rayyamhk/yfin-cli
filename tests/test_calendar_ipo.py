"""Tests for the calendar-ipo command."""

import pandas as pd
from unittest.mock import patch


def create_mock_ipo_data():
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


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_ipo_basic(mock_calendars, invoke_json):
    mock_calendars.return_value.get_ipo_info_calendar.return_value = (
        create_mock_ipo_data()
    )
    code, data = invoke_json("calendar-ipo")

    assert code == 0
    assert len(data) == 2
    assert data[0]["Company"] == "Tech IPO Inc"
    assert data[0]["Exchange"] == "NASDAQ"


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_ipo_with_options(mock_calendars, invoke_json):
    mock_calendars.return_value.get_ipo_info_calendar.return_value = (
        create_mock_ipo_data()
    )
    code, _ = invoke_json("calendar-ipo", "--limit", "5", "--start", "2026-02-01")

    assert code == 0
    call_kwargs = mock_calendars.return_value.get_ipo_info_calendar.call_args[1]
    assert call_kwargs["limit"] == 5
    assert call_kwargs["start"] == "2026-02-01"
    assert call_kwargs["end"] == "2026-02-08"


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_ipo_empty_data(mock_calendars, invoke_json):
    mock_calendars.return_value.get_ipo_info_calendar.return_value = pd.DataFrame()
    code, data = invoke_json("calendar-ipo")

    assert code == 0
    assert data == []


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_ipo_none_data(mock_calendars, invoke):
    mock_calendars.return_value.get_ipo_info_calendar.return_value = None
    result = invoke("calendar-ipo")

    assert result.exit_code == 1
    assert "No data found" in result.output


def test_calendar_ipo_invalid_date(invoke):
    result = invoke("calendar-ipo", "--start", "invalid-date")
    assert result.exit_code == 2
    assert "Invalid date format" in result.output


@patch("src.commands.calendar.yf.Calendars")
def test_calendar_ipo_api_error(mock_calendars, invoke):
    mock_calendars.return_value.get_ipo_info_calendar.side_effect = Exception(
        "API Error"
    )
    result = invoke("calendar-ipo")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
