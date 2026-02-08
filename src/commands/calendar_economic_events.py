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
def calendar_economic_events(
    start: StartDateType,
    end: EndDateType,
    limit: LimitType = default_limit,
    offset: OffsetType = default_offset,
    output: OutputType = default_output,
):
    """
    Get economic events calendar.
    """
    kwargs = {"limit": limit, "offset": offset}
    if start:
        kwargs["start"] = start
    if end:
        kwargs["end"] = end

    calendars = yf.Calendars()
    data_frame = calendars.get_economic_events_calendar(**kwargs)
    return data_frame
