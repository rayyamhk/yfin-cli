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


def income_statement(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
    frequency: str = typer.Option(
        "yearly",
        "--frequency",
        "-f",
        help="Frequency of the income statement (yearly, quarterly or trailing)",
    ),
):
    """
    Get income statement for a ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        income_statement = stock.get_income_stmt(pretty=True, freq=frequency)

        if income_statement.empty:
            print_warning(f"No income statement found for {ticker}.")
            raise typer.Exit(code=1)

        _print_income_statement_table(income_statement, ticker)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_income_statement_table(income_statement: pd.DataFrame, ticker: str):
    """Print income statement DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Metric")

    # Add columns for each date
    # Valid Dates are in columns. Sort descending (newest first) is usually default from yfinance
    # but let's ensure or respect existing order.
    dates = income_statement.columns
    for date in dates:
        table.add_column(fmt_date(date))

    # Iterate over rows (Metrics)
    for metric, row in income_statement.iterrows():
        row_values = []
        for val in row:
            row_values.append(fmt_large_number(val))

        table.add_row(metric, *row_values)

    print_table(table)
