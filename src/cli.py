#!/usr/bin/env python3
"""
yfin CLI - A command-line wrapper for yfinance
"""

import typer
from .commands.history import history
from .commands.news import news
from .commands.fast_info import fast_info
from .commands.calendar_earnings import calendar_earnings
from .commands.calendar_ipo import calendar_ipo
from .commands.calendar_economic_events import calendar_economic_events
from .commands.income_statement import income_statement
from .commands.balance_sheet import balance_sheet
from .commands.cashflow import cashflow
from .commands.earnings_dates import earnings_dates

app = typer.Typer(
    name="yfin",
    help="A command-line interface for Yahoo Finance data",
    no_args_is_help=True,
)

app.command(name="history")(history)
app.command(name="news")(news)
app.command(name="fast-info")(fast_info)
app.command(name="calendar-earnings")(calendar_earnings)
app.command(name="calendar-ipo")(calendar_ipo)
app.command(name="calendar-economic-events")(calendar_economic_events)
app.command(name="income-statement")(income_statement)
app.command(name="balance-sheet")(balance_sheet)
app.command(name="cashflow")(cashflow)
app.command(name="earnings-dates")(earnings_dates)

if __name__ == "__main__":
    app()
