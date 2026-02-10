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
from ..decorators import command
from ..utils import compact, data_frame_to_list


@command
def calendar_earnings(
    start: StartDateType,
    end: EndDateType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
    market_cap: MarketCapType = default_market_cap,
):
    """
    Get earnings calendar.
    """
    kwargs = compact(
        limit=limit,
        offset=offset,
        start=start,
        end=end,
        market_cap=market_cap,
    )

    calendars = yf.Calendars()
    data_frame = calendars.get_earnings_calendar(**kwargs)
    return data_frame_to_list(data_frame)


@command
def calendar_economic_events(
    start: StartDateType,
    end: EndDateType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
):
    """
    Get economic events calendar.
    """
    kwargs = compact(
        limit=limit,
        offset=offset,
        start=start,
        end=end,
    )

    calendars = yf.Calendars()
    data_frame = calendars.get_economic_events_calendar(**kwargs)
    return data_frame_to_list(data_frame)


@command
def calendar_ipo(
    start: StartDateType,
    end: EndDateType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
):
    """
    Get IPO calendar.
    """
    kwargs = compact(
        limit=limit,
        offset=offset,
        start=start,
        end=end,
    )

    calendars = yf.Calendars()
    data_frame = calendars.get_ipo_info_calendar(**kwargs)
    return data_frame_to_list(data_frame)
