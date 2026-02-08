import yfinance as yf
import typer
from typing import Annotated
from ..typer import (
    TickerType,
    IntervalType,
    default_interval,
    OutputType,
    default_output,
)
from ..validator import validate_period, validate_date_string
from ..decorators import handle_errors, with_output
from ..utils import count_specified


@handle_errors
@with_output
def history(
    ticker: TickerType,
    interval: IntervalType = default_interval,
    period: Annotated[
        str | None,
        typer.Option(
            callback=lambda x: validate_period(x) if x else None,
            help="Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
        ),
    ] = None,
    start: Annotated[
        str | None,
        typer.Option(
            callback=lambda x: validate_date_string(x) if x else None,
            help="Start date (YYYY-MM-DD)",
        ),
    ] = None,
    end: Annotated[
        str | None,
        typer.Option(
            callback=lambda x: validate_date_string(x) if x else None,
            help="End date (YYYY-MM-DD)",
        ),
    ] = None,
    output: OutputType = default_output,
):
    """
    Get historical market data for a stock ticker.

    Note: period, start, and end - at most 2 of these can be specified together.
    """
    specified_count = count_specified(period, start, end)
    if specified_count > 2:
        raise typer.BadParameter(
            "At most 2 of --period, --start, --end can be specified together."
        )

    if specified_count == 0:
        period = "1mo"

    kwargs = {"interval": interval}
    if period is not None:
        kwargs["period"] = period
    if start is not None:
        kwargs["start"] = start
    if end is not None:
        kwargs["end"] = end

    stock = yf.Ticker(ticker)
    data_frame = stock.history(**kwargs)
    return data_frame
