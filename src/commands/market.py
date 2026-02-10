import yfinance as yf
from ..typer import (
    StartDateType,
    EndDateType,
    LimitType,
    default_limit,
    OffsetType,
    default_offset,
    MarketCapType,
    default_market_cap,
)
from ..decorators import handle_errors, with_output
from ..utils import data_frame_to_list


@handle_errors
@with_output
def market_status():
    """
    Get the US market status.
    """
    market = yf.Market("US")
    return market.status
