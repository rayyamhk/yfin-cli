import yfinance as yf
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def market_status():
    """
    Get the US market status.
    """
    market = yf.Market("US")
    return market.status
