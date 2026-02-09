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
    sector_keys,
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
from .commands.screen import (
    screen,
    screen_query_fields,
    screen_query_values,
    screen_predefined_queries,
)

app = typer.Typer(
    name="yfin",
    help="A command-line interface for Yahoo Finance data",
    no_args_is_help=True,
)


@app.callback()
def main(ctx: typer.Context, output: OutputType = default_output):
    ctx.ensure_object(dict)
    ctx.obj["output"] = output


app.command(rich_help_panel="Stock")(history)
app.command(rich_help_panel="Stock")(dividends)
app.command(rich_help_panel="Stock")(fast_info)
app.command(rich_help_panel="Stock")(news)

app.command(rich_help_panel="Calendar")(calendar_earnings)
app.command(rich_help_panel="Calendar")(calendar_ipo)
app.command(rich_help_panel="Calendar")(calendar_economic_events)

app.command(rich_help_panel="Financials")(income_stmt)
app.command(rich_help_panel="Financials")(balance_sheet)
app.command(rich_help_panel="Financials")(cashflow)
app.command(rich_help_panel="Financials")(earnings_dates)

app.command(rich_help_panel="Analysis")(recommendations)
app.command(rich_help_panel="Analysis")(upgrades_downgrades)
app.command(rich_help_panel="Analysis")(price_targets)
app.command(rich_help_panel="Analysis")(earnings_estimate)
app.command(rich_help_panel="Analysis")(revenue_estimate)
app.command(rich_help_panel="Analysis")(earnings_history)
app.command(rich_help_panel="Analysis")(eps_trend)
app.command(rich_help_panel="Analysis")(eps_revisions)
app.command(rich_help_panel="Analysis")(growth_estimates)
app.command(rich_help_panel="Analysis")(insider_purchases)
app.command(rich_help_panel="Analysis")(insider_transactions)
app.command(rich_help_panel="Analysis")(insider_roster_holders)
app.command(rich_help_panel="Analysis")(major_holders)
app.command(rich_help_panel="Analysis")(institutional_holders)
app.command(rich_help_panel="Analysis")(mutualfund_holders)

app.command(rich_help_panel="Sector")(sector_keys)
app.command(rich_help_panel="Sector")(sector_industries)
app.command(rich_help_panel="Sector")(sector_overview)
app.command(rich_help_panel="Sector")(sector_research_reports)
app.command(rich_help_panel="Sector")(sector_top_companies)
app.command(rich_help_panel="Sector")(sector_top_etfs)
app.command(rich_help_panel="Sector")(sector_top_mutual_funds)

app.command(rich_help_panel="Industry")(industry_overview)
app.command(rich_help_panel="Industry")(industry_research_reports)
app.command(rich_help_panel="Industry")(industry_top_companies)
app.command(rich_help_panel="Industry")(industry_top_growth_companies)
app.command(rich_help_panel="Industry")(industry_top_performing_companies)

app.command(rich_help_panel="Screen")(screen)
app.command(rich_help_panel="Screen")(screen_query_fields)
app.command(rich_help_panel="Screen")(screen_query_values)
app.command(rich_help_panel="Screen")(screen_predefined_queries)

if __name__ == "__main__":
    app()
