import yfinance as yf
from ..decorators import command


@command
def market_status():
    """
    Get the US market status.
    """
    market = yf.Market("US")
    return market.status
