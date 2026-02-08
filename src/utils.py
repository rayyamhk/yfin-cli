from typing import Any
from datetime import datetime, timedelta
from rich.console import Console

console = Console()


def print(content: Any):
    console.print(content)


def print_error(content: Any):
    console.print(f"[red]{content}[/red]")


def count_specified(*args: str | None) -> int:
    """Count the number of specified arguments"""
    return sum(x is not None for x in args)


def increment_datetime_by_days(date: datetime, delta: int) -> datetime:
    return date + timedelta(days=delta)
