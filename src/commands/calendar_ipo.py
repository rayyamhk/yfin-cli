import yfinance as yf
from ..typer import (
    StartDateType,
    EndDateType,
    LimitType,
    default_limit,
    OffsetType,
    default_offset,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def calendar_ipo(
    start: StartDateType,
    end: EndDateType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
    output: OutputType = default_output,
):
    """
    Get IPO calendar.
    """
    kwargs = {"limit": limit, "offset": offset}
    if start:
        kwargs["start"] = start
    if end:
        kwargs["end"] = end

    calendars = yf.Calendars()
    data_frame = calendars.get_ipo_info_calendar(**kwargs)
    return data_frame
