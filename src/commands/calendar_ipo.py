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
    fmt_price,
    fmt_volume,
)


def calendar_ipo(
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
        help="Maximum number of IPOs to show",
    ),
    offset: int = typer.Option(
        0,
        "--offset",
        "-o",
        help="Offset for the IPO calendar",
    ),
):
    """
    Get IPO calendar.
    """
    start, end = validate_date_range(start, end)

    try:
        kwargs = {"limit": limit, "offset": offset}
        if start:
            kwargs["start"] = start
        if end:
            kwargs["end"] = end

        calendars = yf.Calendars()
        # Using get_ipo_info_calendar as get_ipo_calendar does not exist
        ipo_df = calendars.get_ipo_info_calendar(**kwargs)

        if ipo_df.empty:
            print_warning("No IPOs found for the specified criteria.")
            raise typer.Exit(code=1)

        _print_ipo_table(ipo_df)

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


def _print_ipo_table(ipo_df):
    """Print IPO calendar DataFrame as a Rich Table."""
    table = Table()
    table.add_column("Date")
    table.add_column("Symbol")
    table.add_column("Company")
    table.add_column("Exchange")
    table.add_column("Filing Date")
    table.add_column("Amended Date")
    table.add_column("Price From")
    table.add_column("Price To")
    table.add_column("Price")
    table.add_column("Currency")
    table.add_column("Shares")
    table.add_column("Action")

    for symbol, row in ipo_df.iterrows():
        date = fmt_date(row.get("Date"))
        company = fmt_str(row.get("Company"))
        exchange = fmt_str(row.get("Exchange"))
        filing_date = fmt_date(row.get("Filing Date"))
        amended_date = fmt_date(row.get("Amended Date"))
        price_from = fmt_price(row.get("Price From"))
        price_to = fmt_price(row.get("Price To"))
        price = fmt_price(row.get("Price"))
        currency = fmt_str(row.get("Currency"))
        shares = fmt_volume(row.get("Shares"))
        action = fmt_str(row.get("Action"))

        table.add_row(
            date,
            symbol,
            company,
            exchange,
            filing_date,
            amended_date,
            price_from,
            price_to,
            price,
            currency,
            shares,
            action,
        )

    print_table(table)
