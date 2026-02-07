from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
import math
import typer
import pandas as pd

console = Console()


def validate_date(value: str) -> str:
    """Validate date string format (YYYY-MM-DD)"""
    try:
        if len(value) != 10:
            raise ValueError("Invalid date format")
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise typer.BadParameter(f"Invalid date format: {value}. Use YYYY-MM-DD")


def validate_date_range(start: str | None, end: str | None) -> tuple[str, str]:
    """Validate date range and return start and end dates"""
    if not start and not end:
        start = fmt_date(datetime.now())
        end = fmt_date(increment_date(datetime.now(), 7))
    elif not start and end:
        start = fmt_date(increment_date(datetime.fromisoformat(validate_date(end)), -7))
    elif start and not end:
        end = fmt_date(increment_date(datetime.fromisoformat(validate_date(start)), 7))
    else:
        start = validate_date(start)
        end = validate_date(end)

    if datetime.fromisoformat(start) > datetime.fromisoformat(end):
        print_error("Start date must be before end date.")
        raise typer.Exit(code=1)

    return start, end


def count_specified(*args: str | None) -> int:
    """Count the number of specified arguments"""
    return sum(x is not None for x in args)


def validate_choice(choice: str, choices: list[str]):
    if choice not in choices:
        raise typer.BadParameter(
            f"Invalid choice '{choice}'. Choose from: {', '.join(choices)}"
        )
    return choice


def print_warning(msg: str):
    """Print a warning message"""
    console.print(f"[yellow]{msg}[/yellow]")


def print_error(msg: str):
    """Print an error message"""
    console.print(f"[red]{msg}[/red]")


def print_table(table: Table):
    """Print a table"""
    console.print(table)


def is_nonsense(val: any) -> bool:
    """Check if a value is effectively 'empty' or 'nonsense'."""
    if val is None:
        return True

    # Check for pandas/numpy NaN without assuming types
    try:
        if pd.isna(val):
            return True
    except Exception:
        pass

    # Check for math.isnan (only works for numbers)
    if isinstance(val, (int, float)):
        try:
            if math.isnan(val):
                return True
        except Exception:
            pass

    return False


def fmt_str(val: str | None):
    return val if not is_nonsense(val) else "N/A"


def fmt_date_str(val: str | None):
    if is_nonsense(val):
        return "N/A"
    try:
        dt = datetime.fromisoformat(val)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "N/A"


def fmt_date(val: datetime | None):
    return val.strftime("%Y-%m-%d") if not is_nonsense(val) else "N/A"


def fmt_price(val: float | int | None):
    return f"${fmt_decimal(val)}" if not is_nonsense(val) else "N/A"


def fmt_decimal(val: float | int | None):
    return f"{val:,.2f}" if not is_nonsense(val) else "N/A"


def fmt_volume(val: float | int | None):
    return f"{val:,.0f}" if not is_nonsense(val) else "N/A"


def fmt_market_cap(val: float | int | None):
    if is_nonsense(val):
        return "N/A"
    return f"${fmt_large_number(val)}"


def fmt_large_number(val: float | int | None):
    if is_nonsense(val):
        return "N/A"
    if val < 0:
        return f"-{fmt_large_number(abs(val))}"
    if val >= 1e12:
        return f"{val / 1e12:.2f}T"
    if val >= 1e9:
        return f"{val / 1e9:.2f}B"
    if val >= 1e6:
        return f"{val / 1e6:.2f}M"
    if val >= 1e3:
        return f"{val / 1e3:.2f}K"
    return f"{val:,.2f}"


def fmt_percentage(val: float | int | None):
    return f"{val * 100:.2f}%" if not is_nonsense(val) else "N/A"


def increment_date(date: datetime, delta: int) -> datetime:
    return date + timedelta(days=delta)
