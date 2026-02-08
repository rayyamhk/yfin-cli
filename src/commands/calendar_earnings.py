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
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def calendar_earnings(
    start: StartDateType,
    end: EndDateType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
    market_cap: MarketCapType = default_market_cap,
    output: OutputType = default_output,
):
    """
    Get earnings calendar.
    """
    kwargs = {"limit": limit, "offset": offset}
    if start:
        kwargs["start"] = start
    if end:
        kwargs["end"] = end
    if market_cap:
        kwargs["market_cap"] = market_cap

    calendars = yf.Calendars()
    data_frame = calendars.get_earnings_calendar(**kwargs)
    return data_frame
