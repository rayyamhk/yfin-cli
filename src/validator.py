import typer
from datetime import datetime
from pandas import DataFrame


def validate_date_string(value: str) -> str:
    """Validate date string format (YYYY-MM-DD)"""
    try:
        if len(value) != 10:
            raise ValueError()
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise typer.BadParameter(f"Invalid date format: {value}. Use YYYY-MM-DD")


def validate_data_frame_has_data(data: DataFrame) -> DataFrame:
    """Validate that data frame is not empty."""
    if data.empty:
        raise typer.Exit(code=1)
    return data


VALID_OUTPUT_TYPES = ["table"]


def validate_output_type(value: str) -> str:
    """Validate output type"""
    if value not in VALID_OUTPUT_TYPES:
        raise typer.BadParameter(
            f"Invalid output type: {value}. Use {', '.join(VALID_OUTPUT_TYPES)}"
        )
    return value


VALID_FREQUENCIES = ["yearly", "quarterly"]


def validate_frequency(value: str) -> str:
    """Validate frequency"""
    if value not in VALID_FREQUENCIES:
        raise typer.BadParameter(
            f"Invalid frequency: {value}. Use {', '.join(VALID_FREQUENCIES)}"
        )
    return value


VALID_EXTENDED_FREQUENCIES = ["yearly", "quarterly", "trailing"]


def validate_extended_frequency(value: str) -> str:
    """Validate extended frequency"""
    if value not in VALID_EXTENDED_FREQUENCIES:
        raise typer.BadParameter(
            f"Invalid frequency: {value}. Use {', '.join(VALID_EXTENDED_FREQUENCIES)}"
        )
    return value


VALID_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


def validate_period(val: str) -> str:
    """Validate period"""
    if val not in VALID_PERIODS:
        raise typer.BadParameter(
            f"Invalid period: {val}. Use {', '.join(VALID_PERIODS)}"
        )
    return val


VALID_INTERVALS = [
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
]


def validate_interval(val: str) -> str:
    """Validate interval"""
    if val not in VALID_INTERVALS:
        raise typer.BadParameter(
            f"Invalid interval: {val}. Use {', '.join(VALID_INTERVALS)}"
        )
    return val


VALID_NEWS_TABS = ["all", "news", "press releases"]


def validate_news_tab(val: str) -> str:
    """Validate tab"""
    if val not in VALID_NEWS_TABS:
        raise typer.BadParameter(
            f"Invalid tab: {val}. Use {', '.join(VALID_NEWS_TABS)}"
        )
    return val
