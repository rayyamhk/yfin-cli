"""Tests for output-size reductions: number cleanup, null dropping, compact JSON,
row limits, and trimmed screener results."""

import io
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import data_frame_to_list, paginate
from src.writer import JsonWriter, simplify


# ── number cleanup and null dropping ─────────────────────────────────


@pytest.mark.parametrize(
    "value, expected",
    [
        (395.42999267578125, 395.43),  # float32 artifact
        (0.066300005, 0.0663),
        (838588.0, 838588),  # whole number -> int
        (1544895901139.208, 1544895901139),  # large value -> int
        (0.0000123456, 0.0000123456),  # small prices keep precision
        (2.64089, 2.64089),  # real digits untouched
        (float("nan"), None),  # NaN isn't valid JSON
        (float("inf"), None),
    ],
)
def test_simplify_numbers(value, expected):
    assert simplify(value, drop_nulls=False) == expected


def test_simplify_leaves_bools_and_ints_alone():
    assert simplify({"a": True, "b": 7}, drop_nulls=True) == {"a": True, "b": 7}


def test_simplify_drops_nulls_in_nested_objects_only():
    data = [{"a": 1, "b": None, "c": {"d": None, "e": 2.0}}, None]
    assert simplify(data, drop_nulls=True) == [{"a": 1, "c": {"e": 2}}, None]


def test_simplify_keeps_nulls_when_asked():
    assert simplify({"a": None}, drop_nulls=False) == {"a": None}


# ── JSON formatting ───────────────────────────────────────────────────


def _write(data, tty):
    out = io.StringIO()
    out.isatty = lambda: tty
    with patch("sys.stdout", out):
        JsonWriter().write(data)
    return out.getvalue()


def test_json_is_compact_when_piped():
    assert _write({"a": 1, "b": [1, 2]}, tty=False) == '{"a":1,"b":[1,2]}\n'


def test_json_is_pretty_in_a_terminal():
    assert _write({"a": 1}, tty=True) == '{\n  "a": 1\n}\n'


def test_json_keeps_non_ascii_readable():
    assert _write({"name": "Nestlé"}, tty=False) == '{"name":"Nestlé"}\n'


# ── DataFrame conversion ──────────────────────────────────────────────


def test_unnamed_range_index_is_not_output():
    df = pd.DataFrame({"Holder": ["A", "B"]})
    assert data_frame_to_list(df) == [{"Holder": "A"}, {"Holder": "B"}]


def test_meaningful_index_is_kept():
    df = pd.DataFrame({"v": [1]}, index=pd.Index(["0m"], name="period"))
    assert data_frame_to_list(df) == [{"period": "0m", "v": 1}]


# ── row limits ────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "limit, offset, expected",
    [(2, 0, [0, 1]), (2, 3, [3, 4]), (0, 0, [0, 1, 2, 3, 4]), (0, 3, [3, 4])],
)
def test_paginate(limit, offset, expected):
    assert paginate([0, 1, 2, 3, 4], limit, offset) == expected


def _grades(n):
    return pd.DataFrame(
        {"Firm": [f"F{i}" for i in range(n)]},
        index=pd.DatetimeIndex(
            pd.date_range("2026-01-01", periods=n), name="GradeDate"
        ),
    )


@patch("src.commands.analysis.yf.Ticker")
def test_upgrades_downgrades_defaults_to_20_rows(mock_ticker, invoke_json):
    mock_ticker.return_value.get_upgrades_downgrades.return_value = _grades(50)
    code, data = invoke_json("upgrades-downgrades", "AAPL")
    assert code == 0
    assert len(data) == 20


@patch("src.commands.analysis.yf.Ticker")
def test_upgrades_downgrades_limit_offset_and_all(mock_ticker, invoke_json):
    mock_ticker.return_value.get_upgrades_downgrades.return_value = _grades(50)
    _, page = invoke_json(
        "upgrades-downgrades", "AAPL", "--limit", "2", "--offset", "5"
    )
    _, everything = invoke_json("upgrades-downgrades", "AAPL", "--limit", "0")
    assert [r["Firm"] for r in page] == ["F5", "F6"]
    assert len(everything) == 50


@patch("src.commands.financials.yf.Ticker")
def test_sec_filings_limited_and_trimmed(mock_ticker, invoke_json):
    mock_ticker.return_value.get_sec_filings.return_value = [
        {
            "date": "2026-11-0%d" % (i % 9 + 1),
            "type": "8-K",
            "epochDate": 1,
            "maxAge": 1,
            "exhibits": {},
        }
        for i in range(30)
    ]
    code, data = invoke_json("sec-filings", "AAPL")
    assert code == 0
    assert len(data) == 20
    assert data[0] == {"date": "2026-11-01", "type": "8-K"}


# ── history corporate-action columns ─────────────────────────────────


def _bars(dividends):
    return pd.DataFrame(
        {"Close": [1.0, 2.0], "Dividends": dividends, "Stock Splits": [0.0, 0.0]},
        index=pd.DatetimeIndex(["2026-11-05", "2026-11-06"], name="Date"),
    )


@patch("src.commands.stock.yf.Ticker")
def test_history_drops_all_zero_corporate_action_columns(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = _bars([0.0, 0.0])
    _, data = invoke_json("history", "AAPL")
    assert data[0] == {"Date": "2026-11-05", "Close": 1}


@patch("src.commands.stock.yf.Ticker")
def test_history_keeps_dividends_when_paid_in_range(mock_ticker, invoke_json):
    mock_ticker.return_value.history.return_value = _bars([0.0, 0.26])
    _, data = invoke_json("history", "AAPL")
    assert [r["Dividends"] for r in data] == [0, 0.26]
    assert "Stock Splits" not in data[0]


# ── screener fields ──────────────────────────────────────────────────

FULL_QUOTE = {
    "symbol": "AAPL",
    "longName": "Apple Inc.",
    "regularMarketPrice": 355.63,
    "trailingPE": 30.1,
    "triggerable": False,
    "messageBoardId": "finmb_24937",
}


@patch("src.commands.screen.yf.screen")
def test_screen_returns_summary_fields_by_default(mock_screen, invoke_json):
    mock_screen.return_value = {"quotes": [FULL_QUOTE]}
    _, data = invoke_json("screen", "--filter", "region eq us")
    assert data == [
        {
            "symbol": "AAPL",
            "longName": "Apple Inc.",
            "regularMarketPrice": 355.63,
            "trailingPE": 30.1,
        }
    ]


@patch("src.commands.screen.yf.screen")
def test_screen_fields_option_picks_fields_and_keeps_symbol(mock_screen, invoke_json):
    mock_screen.return_value = {"quotes": [FULL_QUOTE]}
    _, data = invoke_json(
        "screen", "--filter", "region eq us", "--fields", "trailingPE, nope"
    )
    assert data == [{"symbol": "AAPL", "trailingPE": 30.1}]


@patch("src.commands.screen.yf.screen")
def test_screen_all_fields_returns_everything(mock_screen, invoke_json):
    mock_screen.return_value = {"quotes": [FULL_QUOTE]}
    _, data = invoke_json("screen", "--filter", "region eq us", "--all-fields")
    assert data == [FULL_QUOTE]


def test_screen_fields_and_all_fields_are_exclusive(invoke):
    result = invoke(
        "screen", "--filter", "region eq us", "--fields", "x", "--all-fields"
    )
    assert result.exit_code == 2
    assert "mutually exclusive" in result.output
