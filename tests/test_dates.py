"""Tests for date formatting in JSON output: no shifting to UTC."""

import pandas as pd

from src.utils import data_frame_to_list, series_to_list


def _daily(tz):
    index = pd.DatetimeIndex(["2026-11-06", "2026-11-09"], name="Date").tz_localize(tz)
    return pd.DataFrame({"Close": [1.0, 2.0]}, index=index)


def test_daily_bars_east_of_utc_keep_their_exchange_date():
    # Midnight Tokyo is 15:00 UTC the previous day; it must not shift.
    rows = data_frame_to_list(_daily("Asia/Tokyo"))
    assert [r["Date"] for r in rows] == ["2026-11-06", "2026-11-09"]


def test_daily_bars_west_of_utc_are_plain_dates():
    rows = data_frame_to_list(_daily("America/New_York"))
    assert [r["Date"] for r in rows] == ["2026-11-06", "2026-11-09"]


def test_intraday_bars_keep_time_and_exchange_offset():
    index = pd.DatetimeIndex(
        ["2026-11-12 09:00", "2026-11-12 10:00"], name="Datetime"
    ).tz_localize("Asia/Tokyo")
    rows = data_frame_to_list(pd.DataFrame({"Close": [1.0, 2.0]}, index=index))
    assert [r["Datetime"] for r in rows] == [
        "2026-11-12T09:00:00+09:00",
        "2026-11-12T10:00:00+09:00",
    ]


def test_naive_midnights_are_plain_dates():
    df = pd.DataFrame({"Reported": pd.to_datetime(["2026-06-30", "2026-03-31"])})
    assert [r["Reported"] for r in data_frame_to_list(df)] == [
        "2026-06-30",
        "2026-03-31",
    ]


def test_naive_timestamps_keep_time():
    df = pd.DataFrame({"At": pd.to_datetime(["2026-11-11 13:02:36"])})
    assert data_frame_to_list(df)[0]["At"] == "2026-11-11T13:02:36"


def test_missing_dates_are_null():
    df = pd.DataFrame({"At": pd.to_datetime(["2026-11-11", None])})
    assert [r["At"] for r in data_frame_to_list(df)] == ["2026-11-11", None]


def test_series_dates_are_not_shifted():
    index = pd.DatetimeIndex(["2026-03-30"], name="Date").tz_localize("Asia/Tokyo")
    rows = series_to_list(pd.Series([47.0], index=index, name="Dividends"))
    assert rows == [{"Date": "2026-03-30", "Dividends": 47.0}]
