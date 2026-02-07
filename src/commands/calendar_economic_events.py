import typer
import yfinance as yf
from rich.table import Table
from ..utils import (
    validate_date_range,
    print_warning,
    print_error,
    print_table,
    fmt_date,
    fmt_str,
    fmt_decimal,
)


def calendar_economic_events(
    start: str | None = typer.Option(
        None,
        "--start",
        "-s",
        help="Start date (YYYY-MM-DD), default today if end is not provided, otherwise 7 days before end",
    ),
    end: str | None = typer.Option(
        None,
        "--end",
        "-e",
        help="End date (YYYY-MM-DD), default 7 days from start",
    ),
    limit: int = typer.Option(
        12,
        "--limit",
        "-l",
        help="Maximum number of events to show",
    ),
    offset: int = typer.Option(
        0,
        "--offset",
        "-o",
        help="Offset for the economic calendar",
    ),
):
    """
    Get economic events calendar.
    """
    start, end = validate_date_range(start, end)

    try:
        kwargs = {"limit": limit, "offset": offset}
        if start:
            kwargs["start"] = start
        if end:
            kwargs["end"] = end

        calendars = yf.Calendars()
        events_df = calendars.get_economic_events_calendar(**kwargs)

        if events_df.empty:
            print_warning("No economic events found for the specified criteria.")
            raise typer.Exit(code=1)

        _print_economic_events_table(events_df)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_economic_events_table(events_df):
    """Print economic events calendar DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Date")
    table.add_column("Event")
    table.add_column("Region")
    table.add_column("For")
    table.add_column("Actual")
    table.add_column("Expected")
    table.add_column("Last")
    table.add_column("Revised")

    # Reset index to get 'Event' name (which is the index) as a column if needed
    # But yfinance returns it as index.

    for event_name, row in events_df.iterrows():
        date = fmt_date(row.get("Event Time"))
        region = fmt_str(row.get("Region"))
        period = fmt_str(row.get("For"))
        actual = fmt_decimal(row.get("Actual"))
        expected = fmt_decimal(row.get("Expected"))
        last = fmt_decimal(row.get("Last"))
        revised = fmt_decimal(row.get("Revised"))

        table.add_row(
            date,
            event_name,
            region,
            period,
            actual,
            expected,
            last,
            revised,
        )

    print_table(table)
