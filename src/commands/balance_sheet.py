import yfinance as yf
from ..typer import (
    TickerType,
    FrequencyType,
    default_frequency,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def balance_sheet(
    ticker: TickerType,
    frequency: FrequencyType = default_frequency,
    output: OutputType = default_output,
):
    """
    Get balance sheet for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_balance_sheet(pretty=True, freq=frequency)
    return data_frame
