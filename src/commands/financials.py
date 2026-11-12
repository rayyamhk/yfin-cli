import yfinance as yf
from ..typer import (
    TickerType,
    FrequencyType,
    ExtendedFrequencyType,
    default_frequency,
    OffsetType,
    default_offset,
    default_limit,
    EarningsDatesLimitType,
    RecentLimitType,
    default_recent_limit,
)
from ..utils import data_frame_to_list, paginate
from ..decorators import command


@command
def income_stmt(
    ticker: TickerType,
    frequency: ExtendedFrequencyType = default_frequency,
):
    """
    Get income statement for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_income_stmt(pretty=True, freq=frequency)
    if data_frame is None:
        return None
    return data_frame_to_list(data_frame.T, index_name="Date")


@command
def balance_sheet(
    ticker: TickerType,
    frequency: FrequencyType = default_frequency,
):
    """
    Get balance sheet for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_balance_sheet(pretty=True, freq=frequency)
    if data_frame is None:
        return None
    return data_frame_to_list(data_frame.T, index_name="Date")


@command
def cashflow(
    ticker: TickerType,
    frequency: ExtendedFrequencyType = default_frequency,
):
    """
    Get cash flow statement for a ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_cashflow(pretty=True, freq=frequency)
    if data_frame is None:
        return None
    return data_frame_to_list(data_frame.T, index_name="Date")


@command
def earnings_dates(
    ticker: TickerType,
    limit: EarningsDatesLimitType = default_limit,
    offset: OffsetType = default_offset,
):
    """
    Get earnings dates, estimates, and reported EPS for a ticker.
    """
    stock = yf.Ticker(ticker)
    # yfinance applies offset on Yahoo's side but rounds limit up to a page
    # size (25, 50 or 100) and returns the whole page, so trim it here.
    data_frame = stock.get_earnings_dates(limit=limit, offset=offset)
    if data_frame is not None:
        data_frame = data_frame.head(limit)
    return data_frame_to_list(data_frame)


@command
def sec_filings(
    ticker: TickerType,
    limit: RecentLimitType = default_recent_limit,
    offset: OffsetType = default_offset,
):
    """
    Get SEC filings for a ticker.
    """
    stock = yf.Ticker(ticker)
    filings = paginate(stock.get_sec_filings(), limit, offset)
    if filings is None:
        return None
    # epochDate duplicates date; maxAge is Yahoo cache metadata.
    return [
        {
            k: v
            for k, v in filing.items()
            if k not in ("epochDate", "maxAge") and not (k == "exhibits" and not v)
        }
        for filing in filings
    ]
