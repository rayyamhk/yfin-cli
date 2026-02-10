import json
import typer
from typing import Any, Callable
from datetime import datetime, timedelta
from pandas import DataFrame, Series
from rich.console import Console

console = Console()


def console_print(content: Any):
    console.print(content)


def console_print_error(content: Any):
    console.print(f"[red]{content}[/red]")


def console_print_warning(content: Any):
    console.print(f"[yellow]{content}[/yellow]")


def count_specified(*args: str | None) -> int:
    """Count the number of specified arguments"""
    return sum(x is not None for x in args)


def compact(**kwargs):
    """Return a dict with None values removed."""
    return {k: v for k, v in kwargs.items() if v is not None}


def get_today_date_string() -> str:
    return format_datetime(datetime.now())


def get_seven_days_from_today_date_string() -> str:
    return format_datetime(datetime.now() + timedelta(days=7))


def format_datetime(val: datetime) -> str:
    return val.strftime("%Y-%m-%d")


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def data_frame_to_list(data_frame: DataFrame, index_name: str | None = None) -> list:
    if data_frame is None:
        return None
    return json.loads(
        data_frame.reset_index(names=index_name).to_json(
            orient="records", date_format="iso"
        )
    )


def series_to_list(series: Series) -> list:
    if series is None:
        return None
    return json.loads(series.reset_index().to_json(orient="records", date_format="iso"))


def validate_value_in_list(valid_values: list[str]) -> Callable[[str], str]:
    def _validator(x: str) -> str:
        if x in valid_values:
            return x
        raise typer.BadParameter(f"Invalid value: {x}")

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
