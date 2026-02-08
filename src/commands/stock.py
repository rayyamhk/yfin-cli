import yfinance as yf
import typer
from typing import Annotated
from ..typer import (
    TickerType,
    IntervalType,
    default_interval,
    NewsTabType,
    default_news_tab,
    CountType,
    default_count,
)
from ..validator import validate_period, VALID_PERIODS, validate_date_string
from ..decorators import handle_errors, with_output
from ..utils import count_specified


@handle_errors
@with_output
def history(
    ticker: TickerType,
    interval: IntervalType = default_interval,
    period: Annotated[
        str | None,
        typer.Option(
            callback=lambda x: validate_period(x) if x else None,
            help=f"Data period {', '.join(VALID_PERIODS)}",
        ),
    ] = None,
    start: Annotated[
        str | None,
        typer.Option(
            callback=lambda x: validate_date_string(x) if x else None,
            help="Start date (YYYY-MM-DD)",
        ),
    ] = None,
    end: Annotated[
        str | None,
        typer.Option(
            callback=lambda x: validate_date_string(x) if x else None,
            help="End date (YYYY-MM-DD)",
        ),
    ] = None,
):
    """
    Get historical market data for a stock ticker.

    Note: period, start, and end - at most 2 of these can be specified together.
    """
    specified_count = count_specified(period, start, end)
    if specified_count > 2:
        raise typer.BadParameter(
            "At most 2 of --period, --start, --end can be specified together."
        )

    if specified_count == 0:
        period = "1mo"

    kwargs = {"interval": interval}
    if period is not None:
        kwargs["period"] = period
    if start is not None:
        kwargs["start"] = start
    if end is not None:
        kwargs["end"] = end

    stock = yf.Ticker(ticker)
    data_frame = stock.history(**kwargs)
    return data_frame


@handle_errors
@with_output
def dividends(
    ticker: TickerType,
    period: Annotated[
        str,
        typer.Option(
            callback=validate_period,
            help=f"Data period {', '.join(VALID_PERIODS)}",
        ),
    ] = "max",
):
    """
    Get dividends for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_dividends(period=period)
    return data_frame


@handle_errors
@with_output
def fast_info(
    ticker: TickerType,
):
    """
    Get fast info summary for a stock ticker.

    Returns key metrics like price, market cap, volume, and 52-week range.
    """
    stock = yf.Ticker(ticker)
    fast_info_dict = dict(stock.get_fast_info())  # fast_info is a dict-like object
    return fast_info_dict


@handle_errors
@with_output
def news(
    ticker: TickerType,
    count: CountType = default_count,
    tab: NewsTabType = default_news_tab,
):
    """
    Get news for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    news_list = stock.get_news(count, tab)
    processed_news_list = []
    for article in news_list:
        content = article.get("content") or {}
        processed_news_list.append(
            {
                "Date": content.get("pubDate"),
                "Title": content.get("title"),
                "Summary": content.get("summary"),
                "URL": (content.get("canonicalUrl") or {}).get("url"),
                "Source": (content.get("provider") or {}).get("displayName"),
            }
        )

    return processed_news_list
