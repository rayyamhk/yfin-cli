import json
import typer
from typing import Any, Callable
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame, Series
from rich.console import Console

console = Console()
# Errors and warnings go to stderr so stdout only ever carries command output.
err_console = Console(stderr=True)


def console_print(content: Any):
    console.print(content)


def console_print_error(content: Any):
    err_console.print(f"[red]{content}[/red]")


def console_print_warning(content: Any):
    err_console.print(f"[yellow]{content}[/yellow]")


def count_specified(*args: str | None) -> int:
    """Count the number of specified arguments"""
    return sum(x is not None for x in args)


def compact(**kwargs):
    """Return a dict with None values removed."""
    return {k: v for k, v in kwargs.items() if v is not None}


def get_today_date_string() -> str:
    return format_datetime(datetime.now())


def default_end_from_start(start: str, end: str | None) -> str:
    if end is not None:
        return end
    start_date = datetime.strptime(start, "%Y-%m-%d")
    return format_datetime(start_date + timedelta(days=7))


def format_datetime(val: datetime) -> str:
    return val.strftime("%Y-%m-%d")


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def _format_datetime_column(column: Series) -> Series:
    """Format a datetime column as strings, in its own timezone.

    pandas' to_json converts timezone-aware values to UTC, which shifts
    exchange-local midnights onto the previous day for markets east of UTC
    (a Tokyo daily bar for Nov 6 becomes "2026-11-05T15:00:00Z").

    Columns where every value is midnight (daily bars, statement periods,
    dividend dates) become plain dates. Anything with a time of day keeps it,
    with its UTC offset when the data is timezone-aware.
    """
    values = column.dropna()
    if values.empty or (values == values.dt.normalize()).all():
        formatted = column.dt.strftime("%Y-%m-%d")
    else:
        formatted = column.map(lambda ts: ts.isoformat() if pd.notna(ts) else None)
    return formatted.astype(object).where(column.notna(), None)


def _records(data_frame: DataFrame) -> list:
    data_frame = data_frame.copy()
    for i in range(data_frame.shape[1]):
        column = data_frame.iloc[:, i]
        if pd.api.types.is_datetime64_any_dtype(column):
            data_frame.isetitem(i, _format_datetime_column(column))
    return json.loads(data_frame.to_json(orient="records", date_format="iso"))


def data_frame_to_list(data_frame: DataFrame, index_name: str | None = None) -> list:
    if data_frame is None:
        return None
    return _records(data_frame.reset_index(names=index_name))


def series_to_list(series: Series) -> list:
    if series is None:
        return None
    return _records(series.reset_index())


def validate_value_in_list(valid_values: list[str]) -> Callable[[str], str]:
    def _validator(x: str) -> str:
        if x in valid_values:
            return x
        raise typer.BadParameter(
            f"Invalid value: {x}, should be one of {', '.join(valid_values)}"
        )

    return _validator


def validate_date_string(value: str) -> str:
    """Validate date string format (YYYY-MM-DD)"""
    try:
        if len(value) != 10:
            raise ValueError()
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise typer.BadParameter(f"Invalid date format: {value}. Use YYYY-MM-DD")
