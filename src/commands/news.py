import yfinance as yf
from pandas import DataFrame
from ..typer import (
    TickerType,
    CountType,
    default_count,
    NewsTabType,
    default_news_tab,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def news(
    ticker: TickerType,
    count: CountType = default_count,
    tab: NewsTabType = default_news_tab,
    output: OutputType = default_output,
):
    """
    Get news for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    news = stock.get_news(count, tab)
    processed_news = []
    for article in news:
        content = article.get("content") or {}
        processed_news.append(
            {
                "Date": content.get("pubDate"),
                "Title": content.get("title"),
                "Summary": content.get("summary"),
                "URL": (content.get("canonicalUrl") or {}).get("url"),
                "Source": (content.get("provider") or {}).get("displayName"),
            }
        )

    data_frame = DataFrame(processed_news)
    return data_frame
