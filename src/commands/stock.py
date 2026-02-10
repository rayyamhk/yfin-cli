import yfinance as yf
import typer
from ..typer import (
    TickerType,
    IntervalType,
    default_interval,
    StartDateTypeOptional,
    EndDateTypeOptional,
    PeriodTypeOptional,
    PeriodType,
    default_period,
    NewsTabType,
    default_news_tab,
    CountType,
    default_count,
)
from ..decorators import command
from ..utils import count_specified, compact, data_frame_to_list, series_to_list


@command
def history(
    ticker: TickerType,
    interval: IntervalType = default_interval,
    period: PeriodTypeOptional = None,
    start: StartDateTypeOptional = None,
    end: EndDateTypeOptional = None,
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

    kwargs = compact(
        interval=interval,
        period=period,
        start=start,
        end=end,
    )

    stock = yf.Ticker(ticker)
    data_frame = stock.history(**kwargs)
    return data_frame_to_list(data_frame)


@command
def dividends(
    ticker: TickerType,
    period: PeriodType = default_period,
):
    """
    Get dividends for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    series = stock.get_dividends(period=period)
    return series_to_list(series)


@command
def fast_info(
    ticker: TickerType,
):
    """
    Get fast info (15 min delayed) summary for a stock ticker.

    Returns key metrics like price, market cap, volume, and 52-week range.
    """
    stock = yf.Ticker(ticker)
    fast_info = stock.get_fast_info()
    if fast_info is None:
        return None
    fast_info_dict = dict(fast_info)  # fast_info is a dict-like object
    return fast_info_dict


@command
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
