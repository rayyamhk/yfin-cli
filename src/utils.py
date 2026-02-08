from typing import Any
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


def format_datetime(val: datetime):
    return val.strftime("%Y-%m-%d")


def increment_datetime_by_days(date: datetime, delta: int) -> datetime:
    return date + timedelta(days=delta)
