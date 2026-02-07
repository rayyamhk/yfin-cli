import typer
import yfinance as yf
from rich.table import Table
from ..utils import (
    print_warning,
    print_error,
    print_table,
    fmt_str,
    fmt_price,
    fmt_volume,
    fmt_market_cap,
    fmt_percentage,
)


def fast_info(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
):
    """
    Get fast info summary for a stock ticker.

    Returns key metrics like price, market cap, volume, and 52-week range.
    """
    ticker = ticker.upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.get_fast_info()

        if not info:
            print_warning(f"No info found for {ticker}")
            raise typer.Exit(code=1)

        _print_fast_info_table(ticker, info)
    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_fast_info_table(ticker: str, info):
    """Print fast info as a Rich Table."""
    table = Table()
    table.add_column("Metric")
    table.add_column("Value")

    # Add rows for each metric
    rows = [
        ("Currency", fmt_str(info.get("currency"))),
        ("Last Price", fmt_price(info.get("lastPrice"))),
        ("Last Volume", fmt_volume(info.get("lastVolume"))),
        ("Open", fmt_price(info.get("open"))),
        ("Previous Close", fmt_price(info.get("previousClose"))),
        ("Day High", fmt_price(info.get("dayHigh"))),
        ("Day Low", fmt_price(info.get("dayLow"))),
        ("52-Week High", fmt_price(info.get("yearHigh"))),
        ("52-Week Low", fmt_price(info.get("yearLow"))),
        ("52-Week Change", fmt_percentage(info.get("yearChange"))),
        ("Market Cap", fmt_market_cap(info.get("marketCap"))),
        ("Shares Outstanding", fmt_volume(info.get("shares"))),
        ("10-Day Avg Volume", fmt_volume(info.get("tenDayAverageVolume"))),
        ("3-Month Avg Volume", fmt_volume(info.get("threeMonthAverageVolume"))),
        ("50-Day Average", fmt_price(info.get("fiftyDayAverage"))),
        ("200-Day Average", fmt_price(info.get("twoHundredDayAverage"))),
        ("Exchange", fmt_str(info.get("exchange"))),
        ("Quote Type", fmt_str(info.get("quoteType"))),
        ("Timezone", fmt_str(info.get("timezone"))),
    ]

    for metric, value in rows:
        table.add_row(metric, str(value))

    print_table(table)
