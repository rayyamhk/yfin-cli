import typer
import pandas as pd
import yfinance as yf
from rich.table import Table
from ..utils import (
    print_warning,
    print_error,
    print_table,
    fmt_date,
    fmt_large_number,
)


def cashflow(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
    frequency: str = typer.Option(
        "yearly",
        "--frequency",
        "-f",
        help="Frequency of the cash flow statement (yearly, quarterly or trailing)",
    ),
):
    """
    Get cash flow statement for a ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        cashflow = stock.get_cashflow(pretty=True, freq=frequency)

        if cashflow.empty:
            print_warning(f"No cash flow statement found for {ticker}.")
            raise typer.Exit(code=1)

        _print_cashflow_table(cashflow)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_cashflow_table(cashflow: pd.DataFrame):
    """Print cash flow DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Metric")

    # Add columns for each date
    dates = cashflow.columns
    for date in dates:
        # For trailing 12 months, the column might not be a timestamp but a string "TTM" or similar?
        # yfinance usually returns dates, but for TTM it might differ.
        # fmt_date handles strings robustly now.
        table.add_column(fmt_date(date))

    # Iterate over rows (Metrics)
    for metric, row in cashflow.iterrows():
        row_values = []
        for val in row:
            row_values.append(fmt_large_number(val))

        table.add_row(metric, *row_values)

    print_table(table)
