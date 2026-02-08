import yfinance as yf
from pandas import DataFrame
from ..typer import (
    TickerType,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def fast_info(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get fast info summary for a stock ticker.

    Returns key metrics like price, market cap, volume, and 52-week range.
    """
    stock = yf.Ticker(ticker)
    fast_info = dict(stock.get_fast_info())  # fast_info is a dict-like object
    data_frame = DataFrame(list(fast_info.items()), columns=["Metric", "Value"])
    return data_frame
