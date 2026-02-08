import typer
from datetime import datetime


def validate_date_string(value: str) -> str:
    """Validate date string format (YYYY-MM-DD)"""
    try:
        if len(value) != 10:
            raise ValueError()
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise typer.BadParameter(f"Invalid date format: {value}. Use YYYY-MM-DD")


VALID_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


def validate_period(val: str) -> str:
    """Validate period"""
    if val not in VALID_PERIODS:
        raise typer.BadParameter(
            f"Invalid period: {val}. Use {', '.join(VALID_PERIODS)}"
        )
    return val
