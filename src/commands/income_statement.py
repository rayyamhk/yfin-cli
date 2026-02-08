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
def income_statement(
    ticker: TickerType,
    frequency: ExtendedFrequencyType = default_frequency,
    output: OutputType = default_output,
):
    """
    Get income statement for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_income_stmt(pretty=True, freq=frequency)
    return data_frame
