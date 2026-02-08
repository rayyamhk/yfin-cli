import yfinance as yf
from ..typer import (
    TickerType,
    LimitType,
    default_limit,
    OffsetType,
    default_offset,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def earnings_dates(
    ticker: TickerType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
    output: OutputType = default_output,
):
    """
    Get earnings dates, estimates, and reported EPS for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_earnings_dates(limit=limit, offset=offset)
    return data_frame
