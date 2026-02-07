import typer
import yfinance as yf
from rich.table import Table
from ..utils import (
    validate_date,
    validate_choice,
    count_specified,
    print_warning,
    print_error,
    print_table,
    fmt_date,
    fmt_price,
    fmt_volume,
)

VALID_INTERVALS = [
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
]
VALID_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


def history(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
    interval: str = typer.Option(
        "1d",
        "--interval",
        "-i",
        help="Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)",
    ),
    period: str | None = typer.Option(
        None,
        "--period",
        "-p",
        help="Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
    ),
    start: str | None = typer.Option(
        None,
        "--start",
        "-s",
        help="Start date (YYYY-MM-DD)",
    ),
    end: str | None = typer.Option(
        None,
        "--end",
        "-e",
        help="End date (YYYY-MM-DD)",
    ),
):
    """
    Get historical market data for a stock ticker.

    Note: period, start, and end - at most 2 of these can be specified together.
    """
    ticker = ticker.upper()
    specified_count = count_specified(period, start, end)
    if specified_count > 2:
        raise typer.BadParameter(
            "At most 2 of --period, --start, --end can be specified together."
        )

    if specified_count == 0:
        period = "1mo"

    try:
        stock = yf.Ticker(ticker)

        kwargs = {"interval": validate_choice(interval, VALID_INTERVALS)}
        if period is not None:
            kwargs["period"] = validate_choice(period, VALID_PERIODS)
        if start is not None:
            kwargs["start"] = validate_date(start)
        if end is not None:
            kwargs["end"] = validate_date(end)

        data = stock.history(**kwargs)
        _print_history_table(ticker, data)
    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_history_table(ticker: str, data):
    """Print stock history DataFrame as a Rich Table."""
    if data.empty:
        print_warning(f"No data found for {ticker}")
        raise typer.Exit(code=1)

    table = Table()
    table.add_column("Date")
    table.add_column("Open")
    table.add_column("High")
    table.add_column("Low")
    table.add_column("Close")
    table.add_column("Volume")

    for date, row in data.iterrows():
        table.add_row(
            fmt_date(date),
            fmt_price(row["Open"]),
            fmt_price(row["High"]),
            fmt_price(row["Low"]),
            fmt_price(row["Close"]),
            fmt_volume(row["Volume"]),
        )

    print_table(table)
