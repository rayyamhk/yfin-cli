import typer
import yfinance as yf
from rich.table import Table
from ..utils import (
    validate_choice,
    print_warning,
    print_error,
    print_table,
    fmt_str,
    fmt_date_str,
)

VALID_TABS = ["all", "news", "press releases"]


def news(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., TSLA, AAPL)"),
    count: int = typer.Option(
        5,
        "--count",
        "-c",
        help="Number of news articles to fetch",
    ),
    tab: str = typer.Option(
        "all",
        "--tab",
        "-t",
        help="News tab (all, news, press releases)",
    ),
):
    """
    Get news for a stock ticker.
    """
    ticker = ticker.upper()
    try:
        stock = yf.Ticker(ticker)
        articles = stock.get_news(count, validate_choice(tab, VALID_TABS))

        if not articles:
            print_warning(f"No news found for {ticker}")
            raise typer.Exit(code=1)

        _print_news_table(ticker, articles)
    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_news_table(ticker: str, articles: list):
    """Print news articles as a Rich Table."""
    table = Table()
    table.add_column("Date")
    table.add_column("Title")
    table.add_column("Summary")
    table.add_column("URL")
    table.add_column("Source")

    for article in articles:
        content = article.get("content", {})
        date = fmt_date_str(content.get("pubDate"))
        title = fmt_str(content.get("title"))
        summary = fmt_str(content.get("summary"))
        url = fmt_str((content.get("canonicalUrl") or {}).get("url"))
        source = fmt_str((content.get("provider") or {}).get("displayName"))

        table.add_row(date, title, summary, url, source)

    print_table(table)
