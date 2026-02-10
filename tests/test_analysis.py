"""Tests for analysis commands (recommendations, estimates, holders, etc.)."""

import pandas as pd
import pytest
from unittest.mock import patch


# ── Mock data factories ───────────────────────────────────────────────


def create_mock_df(columns, rows, index=None):
    """Helper to create simple mock DataFrames."""
    return pd.DataFrame(rows, columns=columns, index=index)


MOCK_RECOMMENDATIONS = create_mock_df(
    columns=["period", "strongBuy", "buy", "hold", "sell", "strongSell"],
    rows=[
        ["0m", 12, 20, 5, 1, 0],
        ["-1m", 10, 18, 6, 2, 1],
    ],
)

MOCK_UPGRADES_DOWNGRADES = create_mock_df(
    columns=["Firm", "ToGrade", "FromGrade", "Action"],
    rows=[
        ["Goldman Sachs", "Buy", "Neutral", "upgrade"],
        ["Morgan Stanley", "Overweight", "Equal-Weight", "upgrade"],
    ],
    index=pd.DatetimeIndex(["2026-02-01", "2026-01-15"]),
)

MOCK_PRICE_TARGETS = {
    "current": 180.0,
    "low": 150.0,
    "high": 220.0,
    "mean": 195.0,
    "median": 192.0,
}

MOCK_ESTIMATES = create_mock_df(
    columns=["avg", "low", "high", "numberOfAnalysts", "growth"],
    rows=[
        [2.10, 1.80, 2.40, 30, 0.15],
        [2.30, 2.00, 2.60, 28, 0.10],
    ],
)

MOCK_EARNINGS_HISTORY = create_mock_df(
    columns=["epsEstimate", "epsActual", "epsDifference", "surprisePercent"],
    rows=[
        [1.50, 1.55, 0.05, 3.3],
        [1.40, 1.42, 0.02, 1.4],
    ],
)

MOCK_HOLDERS_DF = create_mock_df(
    columns=["Holder", "Shares", "Date Reported", "% Out", "Value"],
    rows=[
        ["Vanguard Group", 100000000, "2025-12-31", 7.5, 18000000000],
        ["BlackRock Inc.", 90000000, "2025-12-31", 6.8, 16200000000],
    ],
)

MOCK_MAJOR_HOLDERS = create_mock_df(
    columns=[0, 1],
    rows=[
        [0.07, "% of Shares Held by All Insider"],
        [0.65, "% of Shares Held by Institutions"],
    ],
)

MOCK_INSIDER_PURCHASES = create_mock_df(
    columns=["Shares", "Trans", "Avg Price"],
    rows=[
        [50000, 5, 175.0],
        [30000, 3, 180.0],
    ],
)


# ── DataFrame-based analysis commands ─────────────────────────────────


@pytest.mark.parametrize(
    "command, mock_method, mock_data",
    [
        ("recommendations", "get_recommendations", MOCK_RECOMMENDATIONS),
        ("upgrades-downgrades", "get_upgrades_downgrades", MOCK_UPGRADES_DOWNGRADES),
        ("earnings-estimate", "get_earnings_estimate", MOCK_ESTIMATES),
        ("revenue-estimate", "get_revenue_estimate", MOCK_ESTIMATES),
        ("earnings-history", "get_earnings_history", MOCK_EARNINGS_HISTORY),
        ("eps-trend", "get_eps_trend", MOCK_ESTIMATES),
        ("eps-revisions", "get_eps_revisions", MOCK_ESTIMATES),
        ("growth-estimates", "get_growth_estimates", MOCK_ESTIMATES),
        ("insider-purchases", "get_insider_purchases", MOCK_INSIDER_PURCHASES),
        ("insider-transactions", "get_insider_transactions", MOCK_HOLDERS_DF),
        ("insider-roster-holders", "get_insider_roster_holders", MOCK_HOLDERS_DF),
        ("institutional-holders", "get_institutional_holders", MOCK_HOLDERS_DF),
        ("mutualfund-holders", "get_mutualfund_holders", MOCK_HOLDERS_DF),
    ],
    ids=[
        "recommendations",
        "upgrades_downgrades",
        "earnings_estimate",
        "revenue_estimate",
        "earnings_history",
        "eps_trend",
        "eps_revisions",
        "growth_estimates",
        "insider_purchases",
        "insider_transactions",
        "insider_roster_holders",
        "institutional_holders",
        "mutualfund_holders",
    ],
)
@patch("src.commands.analysis.yf.Ticker")
def test_analysis_df_command_basic(
    mock_ticker, invoke_json, command, mock_method, mock_data
):
    """Test that each DataFrame-based analysis command returns valid JSON."""
    setattr(mock_ticker.return_value, mock_method, lambda: mock_data)
    code, data = invoke_json(command, "AAPL")

    assert code == 0
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.parametrize(
    "command, mock_method",
    [
        ("recommendations", "get_recommendations"),
        ("upgrades-downgrades", "get_upgrades_downgrades"),
        ("earnings-estimate", "get_earnings_estimate"),
        ("revenue-estimate", "get_revenue_estimate"),
        ("earnings-history", "get_earnings_history"),
        ("eps-trend", "get_eps_trend"),
        ("eps-revisions", "get_eps_revisions"),
        ("growth-estimates", "get_growth_estimates"),
        ("insider-purchases", "get_insider_purchases"),
        ("insider-transactions", "get_insider_transactions"),
        ("insider-roster-holders", "get_insider_roster_holders"),
        ("institutional-holders", "get_institutional_holders"),
        ("mutualfund-holders", "get_mutualfund_holders"),
    ],
    ids=[
        "recommendations",
        "upgrades_downgrades",
        "earnings_estimate",
        "revenue_estimate",
        "earnings_history",
        "eps_trend",
        "eps_revisions",
        "growth_estimates",
        "insider_purchases",
        "insider_transactions",
        "insider_roster_holders",
        "institutional_holders",
        "mutualfund_holders",
    ],
)
@patch("src.commands.analysis.yf.Ticker")
def test_analysis_df_command_none_data(mock_ticker, invoke, command, mock_method):
    """Test that each DataFrame-based analysis command handles None gracefully."""
    setattr(mock_ticker.return_value, mock_method, lambda: None)
    result = invoke(command, "AAPL")

    assert result.exit_code == 1
    assert "No data found" in result.output


@pytest.mark.parametrize(
    "command, mock_method",
    [
        ("recommendations", "get_recommendations"),
        ("upgrades-downgrades", "get_upgrades_downgrades"),
        ("earnings-estimate", "get_earnings_estimate"),
        ("revenue-estimate", "get_revenue_estimate"),
        ("earnings-history", "get_earnings_history"),
        ("eps-trend", "get_eps_trend"),
        ("eps-revisions", "get_eps_revisions"),
        ("growth-estimates", "get_growth_estimates"),
        ("insider-purchases", "get_insider_purchases"),
        ("insider-transactions", "get_insider_transactions"),
        ("insider-roster-holders", "get_insider_roster_holders"),
        ("institutional-holders", "get_institutional_holders"),
        ("mutualfund-holders", "get_mutualfund_holders"),
    ],
    ids=[
        "recommendations",
        "upgrades_downgrades",
        "earnings_estimate",
        "revenue_estimate",
        "earnings_history",
        "eps_trend",
        "eps_revisions",
        "growth_estimates",
        "insider_purchases",
        "insider_transactions",
        "insider_roster_holders",
        "institutional_holders",
        "mutualfund_holders",
    ],
)
@patch("src.commands.analysis.yf.Ticker")
def test_analysis_df_command_api_error(mock_ticker, invoke, command, mock_method):
    """Test that each DataFrame-based analysis command handles API errors."""
    setattr(
        mock_ticker.return_value,
        mock_method,
        lambda: (_ for _ in ()).throw(Exception("API Error")),
    )
    result = invoke(command, "AAPL")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output


# ── price-targets (returns dict, not DataFrame) ──────────────────────


@patch("src.commands.analysis.yf.Ticker")
def test_price_targets_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_analyst_price_targets.return_value = MOCK_PRICE_TARGETS
    code, data = invoke_json("price-targets", "AAPL")

    assert code == 0
    assert data["current"] == 180.0
    assert data["low"] == 150.0
    assert data["high"] == 220.0


@patch("src.commands.analysis.yf.Ticker")
def test_price_targets_none_data(mock_ticker, invoke):
    mock_ticker.return_value.get_analyst_price_targets.return_value = None
    result = invoke("price-targets", "AAPL")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.analysis.yf.Ticker")
def test_price_targets_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_analyst_price_targets.side_effect = Exception(
        "API Error"
    )
    result = invoke("price-targets", "AAPL")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output


# ── major-holders (uses index_name="Breakdown") ─────────────────────


@patch("src.commands.analysis.yf.Ticker")
def test_major_holders_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_major_holders.return_value = MOCK_MAJOR_HOLDERS
    code, data = invoke_json("major-holders", "AAPL")

    assert code == 0
    assert isinstance(data, list)
