#!/usr/bin/env python3
"""
yfin CLI - A command-line wrapper for yfinance
"""

import typer
from .commands.analysis import (
    recommendations,
    upgrades_downgrades,
    price_targets,
    earnings_estimate,
    revenue_estimate,
    earnings_history,
    eps_trend,
    eps_revisions,
    growth_estimates,
    insider_purchases,
    insider_transactions,
    insider_roster_holders,
    major_holders,
    institutional_holders,
    mutualfund_holders,
)
from .commands.calendar import (
    calendar_earnings,
    calendar_economic_events,
    calendar_ipo,
)
from .commands.financials import (
    income_stmt,
    balance_sheet,
    cashflow,
    earnings_dates,
)
from .commands.sector import (
    sector_industries,
    sector_overview,
    sector_research_reports,
    sector_top_companies,
    sector_top_etfs,
    sector_top_mutual_funds,
)
from .commands.stock import (
    history,
    dividends,
    fast_info,
    news,
)

app = typer.Typer(
    name="yfin",
    help="A command-line interface for Yahoo Finance data",
    no_args_is_help=True,
)

app.command(name="history")(history)
app.command(name="dividends")(dividends)
app.command(name="fast-info")(fast_info)
app.command(name="news")(news)

app.command(name="calendar-earnings")(calendar_earnings)
app.command(name="calendar-ipo")(calendar_ipo)
app.command(name="calendar-economic-events")(calendar_economic_events)

app.command(name="income_stmt")(income_stmt)
app.command(name="balance-sheet")(balance_sheet)
app.command(name="cashflow")(cashflow)
app.command(name="earnings-dates")(earnings_dates)


app.command(name="recommendations")(recommendations)
app.command(name="upgrades_downgrades")(upgrades_downgrades)
app.command(name="price-targets")(price_targets)
app.command(name="earnings-estimate")(earnings_estimate)
app.command(name="revenue-estimate")(revenue_estimate)
app.command(name="earnings-history")(earnings_history)
app.command(name="eps-trend")(eps_trend)
app.command(name="eps-revisions")(eps_revisions)
app.command(name="growth-estimates")(growth_estimates)
app.command(name="insider-purchases")(insider_purchases)
app.command(name="insider-transactions")(insider_transactions)
app.command(name="insider-roster-holders")(insider_roster_holders)
app.command(name="major-holders")(major_holders)
app.command(name="institutional-holders")(institutional_holders)
app.command(name="mutualfund-holders")(mutualfund_holders)

app.command(name="sector-industries")(sector_industries)
app.command(name="sector-overview")(sector_overview)
app.command(name="sector-research-reports")(sector_research_reports)
app.command(name="sector-top-companies")(sector_top_companies)
app.command(name="sector-top-etfs")(sector_top_etfs)
app.command(name="sector-top-mutual-funds")(sector_top_mutual_funds)

if __name__ == "__main__":
    app()
