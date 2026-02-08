#!/usr/bin/env python3
"""
yfin CLI - A command-line wrapper for yfinance
"""

import typer
from .typer import OutputType, default_output
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
from .commands.industry import (
    industry_overview,
    industry_research_reports,
    industry_top_companies,
    industry_top_growth_companies,
    industry_top_performing_companies,
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

@app.callback()
def main(ctx: typer.Context, output: OutputType=default_output):
    ctx.ensure_object(dict)
    ctx.obj["output"] = output

app.command()(history)
app.command()(dividends)
app.command()(fast_info)
app.command()(news)

app.command()(calendar_earnings)
app.command()(calendar_ipo)
app.command()(calendar_economic_events)

app.command()(income_stmt)
app.command()(balance_sheet)
app.command()(cashflow)
app.command()(earnings_dates)

app.command()(recommendations)
app.command()(upgrades_downgrades)
app.command()(price_targets)
app.command()(earnings_estimate)
app.command()(revenue_estimate)
app.command()(earnings_history)
app.command()(eps_trend)
app.command()(eps_revisions)
app.command()(growth_estimates)
app.command()(insider_purchases)
app.command()(insider_transactions)
app.command()(insider_roster_holders)
app.command()(major_holders)
app.command()(institutional_holders)
app.command()(mutualfund_holders)

app.command()(sector_industries)
app.command()(sector_overview)
app.command()(sector_research_reports)
app.command()(sector_top_companies)
app.command()(sector_top_etfs)
app.command()(sector_top_mutual_funds)

app.command()(industry_overview)
app.command()(industry_research_reports)
app.command()(industry_top_companies)
app.command()(industry_top_growth_companies)
app.command()(industry_top_performing_companies)

if __name__ == "__main__":
    app()
