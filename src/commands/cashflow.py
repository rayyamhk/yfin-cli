import yfinance as yf
from ..typer import (
    TickerType,
    ExtendedFrequencyType,
    default_frequency,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def cashflow(
    ticker: TickerType,
    frequency: ExtendedFrequencyType = default_frequency,
    output: OutputType = default_output,
):
    """
    Get cash flow statement for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_cashflow(pretty=True, freq=frequency)
    return data_frame
