from typing import Any, NoReturn
from datetime import datetime, timedelta
from rich.console import Console

console = Console()


def print(content: Any):
    console.print(content)


def print_error(content: Any):
    console.print(f"[red]{content}[/red]")


def print_warning(content: Any):
    console.print(f"[yellow]{content}[/yellow]")


def count_specified(*args: str | None) -> int:
    """Count the number of specified arguments"""
    return sum(x is not None for x in args)


def format_datetime(val: datetime) -> str:
    return val.strftime("%Y-%m-%d")


def increment_datetime_by_days(date: datetime, delta: int) -> datetime:
    return date + timedelta(days=delta)


def raise_exception(ex: Exception) -> NoReturn:
    raise ex

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def data_frame_to_list(data_frame: DataFrame, index_name: str | None = None) -> list:
    return data_frame.reset_index(names=index_name).to_dict(orient="records")


def series_to_list(series: Series) -> list:
    return series.reset_index().to_dict(orient="records")