import typer
import pandas as pd
import yfinance as yf
from rich.table import Table
from ..utils import (
    print_warning,
    print_error,
    print_table,
    fmt_date,
    fmt_decimal,
    is_nonsense,
)


def earnings_dates(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
    limit: int = typer.Option(12, help="Number of earnings dates to show"),
    offset: int = typer.Option(0, help="Number of earnings dates to skip"),
):
    """
    Get earnings dates, estimates, and reported EPS for a ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        earnings = stock.get_earnings_dates(limit=limit, offset=offset)

        if earnings is None or earnings.empty:
            print_warning(f"No earnings dates found for {ticker}.")
            raise typer.Exit(code=1)

        _print_earnings_dates_table(earnings)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_earnings_dates_table(earnings: pd.DataFrame):
    """Print earnings dates DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Date")
    table.add_column("EPS Estimate")
    table.add_column("Reported EPS")
    table.add_column("Surprise (%)")

    earnings = earnings.sort_index(ascending=False)

    for date, row in earnings.iterrows():
        percentage = row.get(
            "Surprise(%)"
        )  # This is really a percentage (0 - 100) without % sign
        percentage_str = f"{percentage}%" if not is_nonsense(percentage) else "N/A"

        table.add_row(
            fmt_date(date),
            fmt_decimal(row.get("EPS Estimate")),
            fmt_decimal(row.get("Reported EPS")),
            percentage_str,
        )

    print_table(table)
