import typer
import yfinance as yf
from rich.table import Table
from ..utils import (
    validate_date_range,
    print_warning,
    print_error,
    print_table,
    fmt_str,
    fmt_date,
    fmt_decimal,
    fmt_percentage,
    fmt_market_cap,
)


def calendar_earnings(
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
        help="Maximum number of earnings to show",
    ),
    offset: int = typer.Option(
        0,
        "--offset",
        "-o",
        help="Offset for the earnings calendar",
    ),
    market_cap: int | None = typer.Option(
        None,
        "--market-cap",
        "-m",
        help="Filter by market cap",
    ),
):
    """
    Get earnings calendar.
    """
    start, end = validate_date_range(start, end)

    try:
        kwargs = {"limit": limit, "offset": offset}
        if start:
            kwargs["start"] = start
        if end:
            kwargs["end"] = end
        if market_cap:
            kwargs["market_cap"] = market_cap

        calendars = yf.Calendars()
        earnings = calendars.get_earnings_calendar(**kwargs)

        if earnings.empty:
            print_warning("No earnings found for the specified criteria.")
            raise typer.Exit(code=1)

        _print_earnings_table(earnings)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_earnings_table(earnings):
    """Print earnings calendar DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Date")
    table.add_column("Symbol")
    table.add_column("Company")
    table.add_column("Market Cap")
    table.add_column("Event Name")
    table.add_column("Timing")
    table.add_column("EPS Estimate")
    table.add_column("Reported EPS")
    table.add_column("Surprise")

    for symbol, row in earnings.iterrows():
        date = fmt_date(row.get("Event Start Date"))
        company = fmt_str(row.get("Company"))
        market_cap = fmt_market_cap(row.get("Marketcap"))
        event_name = fmt_str(row.get("Event Name"))
        timing = fmt_str(row.get("Timing"))
        eps_estimate = fmt_decimal(row.get("EPS Estimate"))
        reported_eps = fmt_decimal(row.get("Reported EPS"))
        surprise = fmt_percentage(row.get("Surprise(%)"))

        table.add_row(
            date,
            symbol,
            company,
            market_cap,
            event_name,
            timing,
            eps_estimate,
            reported_eps,
            surprise,
        )

    print_table(table)
