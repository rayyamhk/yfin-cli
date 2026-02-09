import yfinance as yf
from ..typer import (
    TickerType,
    FrequencyType,
    ExtendedFrequencyType,
    default_frequency,
    OffsetType,
    default_offset,
    LimitType,
    default_limit,
)
from ..utils import data_frame_to_list
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def income_stmt(
    ticker: TickerType,
    frequency: ExtendedFrequencyType = default_frequency,
):
    """
    Get income statement for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_income_stmt(pretty=True, freq=frequency)
    return data_frame_to_list(data_frame.T, index_name="Date")


@handle_errors
@with_output
def balance_sheet(
    ticker: TickerType,
    frequency: FrequencyType = default_frequency,
):
    """
    Get balance sheet for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_balance_sheet(pretty=True, freq=frequency)
    return data_frame_to_list(data_frame.T, index_name="Date")


@handle_errors
@with_output
def cashflow(
    ticker: TickerType,
    frequency: ExtendedFrequencyType = default_frequency,
):
    """
    Get cash flow statement for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_cashflow(pretty=True, freq=frequency)
    return data_frame_to_list(data_frame.T, index_name="Date")


@handle_errors
@with_output
def earnings_dates(
    ticker: TickerType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
):
    """
    Get earnings dates, estimates, and reported EPS for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_earnings_dates(limit=limit, offset=offset)
    return data_frame_to_list(data_frame)
