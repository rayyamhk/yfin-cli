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


def balance_sheet(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
    frequency: str = typer.Option(
        "yearly",
        "--frequency",
        "-f",
        help="Frequency of the balance sheet (yearly or quarterly)",
    ),
):
    """
    Get balance sheet for a ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        balance_sheet = stock.get_balance_sheet(pretty=True, freq=frequency)

        if balance_sheet.empty:
            print_warning(f"No balance sheet found for {ticker}.")
            raise typer.Exit(code=1)

        _print_balance_sheet_table(balance_sheet)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_balance_sheet_table(balance_sheet: pd.DataFrame):
    """Print balance sheet DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Metric")

    # Add columns for each date
    dates = balance_sheet.columns
    for date in dates:
        table.add_column(fmt_date(date))

    # Iterate over rows (Metrics)
    for metric, row in balance_sheet.iterrows():
        row_values = []
        for val in row:
            row_values.append(fmt_large_number(val))

        table.add_row(metric, *row_values)

    print_table(table)
