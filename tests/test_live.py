"""Live tests: run every command against Yahoo Finance through the installed yfinance.

The rest of the suite mocks yfinance, so it cannot tell when Yahoo changes an
endpoint or a yfinance upgrade changes behavior. These tests can.

Included in a plain `uv run pytest`. Run only these with:

    uv run pytest -m live

Assertions check shape (non-empty JSON with the expected fields), never values,
since market data changes constantly.
"""

import json

import pytest

pytestmark = pytest.mark.live

# A fixed past week, so calendar results don't depend on today's date
# (the current week can legitimately be empty, e.g. around holidays).
PAST_WEEK = ["--start", "2026-10-26", "--end", "2026-10-30"]

OHLCV = {"Open", "High", "Low", "Close", "Volume"}

# (args, expected JSON type, fields every item must have, fields that must be non-null)
CASES = [
    # Stock
    (["history", "AAPL"], list, OHLCV | {"Date"}, {"Close"}),
    (
        ["history", "MSFT", "--period", "5d", "--interval", "5m"],
        list,
        OHLCV | {"Datetime"},
        {"Close"},
    ),
    (["dividends", "KO", "--period", "5y"], list, {"Date", "Dividends"}, {"Dividends"}),
    (
        ["fast-info", "AAPL"],
        dict,
        {"lastPrice", "marketCap", "currency"},
        {"lastPrice"},
    ),
    (
        ["info", "AAPL"],
        dict,
        {"symbol", "longName", "sector", "marketCap"},
        {"longName"},
    ),
    (["news", "AAPL"], list, {"Date", "Title", "URL", "Source"}, {"Title", "URL"}),
    (
        ["news", "AAPL", "--count", "3", "--tab", "press releases"],
        list,
        {"Title", "URL"},
        {"Title"},
    ),
    # Market
    (["market-status"], dict, {"status", "open", "close"}, {"status"}),
    # Calendar
    (
        ["calendar-earnings", *PAST_WEEK, "--limit", "5"],
        list,
        {"Symbol", "Event Start Date"},
        {"Symbol"},
    ),
    (["calendar-ipo", *PAST_WEEK], list, {"Symbol", "Date"}, {"Symbol"}),
    (["calendar-economic-events", *PAST_WEEK], list, {"Event", "Region"}, {"Event"}),
    # Financials
    (["income-stmt", "AAPL"], list, {"Date", "Total Revenue", "Net Income"}, {"Date"}),
    (
        ["income-stmt", "MSFT", "--frequency", "quarterly"],
        list,
        {"Date", "Total Revenue"},
        {"Date"},
    ),
    (
        ["income-stmt", "GOOG", "--frequency", "trailing"],
        list,
        {"Total Revenue"},
        {"Total Revenue"},
    ),
    (["balance-sheet", "AAPL"], list, {"Date", "Total Assets"}, {"Date"}),
    (
        ["cashflow", "NVDA", "--frequency", "quarterly"],
        list,
        {"Date", "Free Cash Flow"},
        {"Date"},
    ),
    (
        ["earnings-dates", "AAPL"],
        list,
        {"Earnings Date", "EPS Estimate"},
        {"Earnings Date"},
    ),
    (["sec-filings", "AAPL"], list, {"date", "type", "title", "edgarUrl"}, {"type"}),
    # Analysis
    (["recommendations", "AAPL"], list, {"period", "buy", "hold", "sell"}, {"period"}),
    (["upgrades-downgrades", "AAPL"], list, {"Firm", "ToGrade", "GradeDate"}, {"Firm"}),
    (["price-targets", "AAPL"], dict, {"current", "mean", "high", "low"}, {"mean"}),
    (["earnings-estimate", "AAPL"], list, {"period", "avg"}, {"period"}),
    (["revenue-estimate", "MSFT"], list, {"period", "avg"}, {"period"}),
    (
        ["earnings-history", "GOOG"],
        list,
        {"quarter", "epsActual", "epsEstimate"},
        {"quarter"},
    ),
    (["eps-trend", "AAPL"], list, {"period", "current"}, {"period"}),
    (["eps-revisions", "NVDA"], list, {"period", "upLast7days"}, {"period"}),
    (["growth-estimates", "AMZN"], list, {"period", "stockTrend"}, {"period"}),
    (
        ["insider-purchases", "AAPL"],
        list,
        {"Insider Purchases Last 6m", "Shares"},
        set(),
    ),
    (["insider-transactions", "TSLA"], list, {"Insider", "Shares"}, {"Insider"}),
    (["insider-roster-holders", "MSFT"], list, {"Name", "Position"}, {"Name"}),
    (["major-holders", "AAPL"], list, {"Breakdown", "Value"}, {"Breakdown"}),
    (["institutional-holders", "GOOG"], list, {"Holder", "Shares"}, {"Holder"}),
    (["mutualfund-holders", "MSFT"], list, {"Holder", "Shares"}, {"Holder"}),
    # Sector
    (["sector-keys"], list, {"key"}, {"key"}),
    (["sector-industries", "technology"], list, {"key", "name"}, {"key"}),
    (
        ["sector-overview", "technology"],
        dict,
        {"companies_count", "market_cap"},
        {"companies_count"},
    ),
    (
        ["sector-research-reports", "financial-services"],
        list,
        {"reportTitle", "provider"},
        {"reportTitle"},
    ),
    (["sector-top-companies", "technology"], list, {"symbol", "name"}, {"symbol"}),
    (["sector-top-etfs", "energy"], list, {"symbol", "name"}, {"symbol"}),
    (["sector-top-mutual-funds", "healthcare"], list, {"symbol", "name"}, {"symbol"}),
    # Industry
    (
        ["industry-overview", "semiconductors"],
        dict,
        {"companies_count", "market_cap"},
        {"companies_count"},
    ),
    (
        ["industry-research-reports", "biotechnology"],
        list,
        {"reportTitle", "provider"},
        {"reportTitle"},
    ),
    (
        ["industry-top-companies", "semiconductors"],
        list,
        {"symbol", "name"},
        {"symbol"},
    ),
    (
        ["industry-top-growth-companies", "software-infrastructure"],
        list,
        {"symbol", "growth estimate"},
        {"symbol"},
    ),
    (
        ["industry-top-performing-companies", "auto-manufacturers"],
        list,
        {"symbol", "ytd return"},
        {"symbol"},
    ),
    # Screen
    (
        ["screen", "--filter", "sector eq Technology", "--filter", "region eq us"],
        list,
        {"symbol"},
        {"symbol"},
    ),
    (["screen", "--predefined", "most_actives"], list, {"symbol"}, {"symbol"}),
    (
        [
            "screen",
            "--json-query",
            '{"operator": "and", "queries": ["region eq us", "intradaymarketcap gte 2000000000"]}',
            "--sort-field",
            "intradaymarketcap",
            "--sort-order",
            "desc",
            "--limit",
            "5",
        ],
        list,
        {"symbol"},
        {"symbol"},
    ),
    (["screen-query-fields"], list, {"field"}, {"field"}),
    (["screen-query-values", "--field", "sector"], list, {"value"}, {"value"}),
    (["screen-predefined-queries"], list, {"query"}, {"query"}),
]


def _run(invoke, args):
    """Run a command, retrying once to ride out transient network errors."""
    result = invoke(*args)
    if result.exit_code != 0:
        result = invoke(*args)
    return result


@pytest.mark.parametrize(
    "args, expected_type, fields, non_null",
    CASES,
    ids=[" ".join(c[0][:3]) for c in CASES],
)
def test_live_command(invoke, args, expected_type, fields, non_null):
    result = _run(invoke, args)
    assert result.exit_code == 0, f"yfin {' '.join(args)} failed:\n{result.output}"

    data = json.loads(result.stdout)
    assert isinstance(data, expected_type), (
        f"expected {expected_type.__name__}, got {type(data).__name__}"
    )
    assert data, "returned no data"

    item = data[0] if isinstance(data, list) else data
    missing = fields - item.keys()
    assert not missing, f"missing fields {sorted(missing)}; got {sorted(item.keys())}"

    nulls = {k for k in non_null if item.get(k) in (None, "")}
    assert not nulls, f"fields unexpectedly empty: {sorted(nulls)}"


def test_live_covers_every_command():
    """Fail if a command is added without a live test."""
    from typer.main import get_command
    from src.cli import app

    registered = set(get_command(app).commands)
    tested = {args[0] for args, *_ in CASES}
    assert registered - tested == set(), (
        f"commands without a live test: {sorted(registered - tested)}"
    )
