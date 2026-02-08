import typer
from datetime import datetime
from typing import Annotated
from .validator import validate_date_string
from .utils import increment_datetime_by_days, format_datetime, raise_exception

TickerType = Annotated[
    str,
    typer.Argument(
        help="Stock ticker symbol (e.g., TSLA, AAPL)", callback=lambda x: x.upper()
    ),
]

VALID_OUTPUT_TYPES = ["raw", "table"]

default_output = VALID_OUTPUT_TYPES[0]

OutputType = Annotated[
    str,
    typer.Option(
        callback=lambda x: (
            x
            if x in VALID_OUTPUT_TYPES
            else raise_exception(typer.BadParameter(f"Invalid output type: {x}"))
        ),
        help=f"Output format ({', '.join(VALID_OUTPUT_TYPES)})",
    ),
]

VALID_FREQUENCIES = ["yearly", "quarterly"]

default_frequency = VALID_FREQUENCIES[0]

FrequencyType = Annotated[
    str,
    typer.Option(
        callback=lambda x: (
            x
            if x in VALID_FREQUENCIES
            else raise_exception(typer.BadParameter(f"Invalid frequency: {x}"))
        ),
        help=f"Frequency of the data ({', '.join(VALID_FREQUENCIES)})",
    ),
]

VALID_EXTENDED_FREQUENCIES = ["yearly", "quarterly", "trailing"]

ExtendedFrequencyType = Annotated[
    str,
    typer.Option(
        callback=lambda x: (
            x
            if x in VALID_EXTENDED_FREQUENCIES
            else raise_exception(typer.BadParameter(f"Invalid frequency: {x}"))
        ),
        help=f"Frequency of the data ({', '.join(VALID_EXTENDED_FREQUENCIES)})",
    ),
]

StartDateType = Annotated[
    str,
    typer.Option(
        default_factory=lambda: format_datetime(datetime.now()),
        callback=validate_date_string,
        help="Start date (YYYY-MM-DD), default today",
    ),
]

EndDateType = Annotated[
    str,
    typer.Option(
        default_factory=lambda: format_datetime(
            increment_datetime_by_days(datetime.now(), 7)
        ),
        callback=validate_date_string,
        help="End date (YYYY-MM-DD), default 7 days from start",
    ),
]

default_limit = 12

LimitType = Annotated[
    int,
    typer.Option(
        help="Maximum number of results to show",
    ),
]

default_offset = 0

OffsetType = Annotated[
    int,
    typer.Option(
        help="Offset of the results",
    ),
]

default_market_cap = 0

MarketCapType = Annotated[
    int,
    typer.Option(
        help="Market cap of the company",
    ),
]

default_interval = "1d"

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

IntervalType = Annotated[
    str,
    typer.Option(
        callback=lambda x: (
            x
            if x in VALID_INTERVALS
            else raise_exception(typer.BadParameter(f"Invalid interval: {x}"))
        ),
        help=f"Data interval ({', '.join(VALID_INTERVALS)})",
    ),
]

default_count = 5

CountType = Annotated[
    int,
    typer.Option(
        help="Number of results to show",
    ),
]

VALID_NEWS_TABS = ["all", "news", "press releases"]

default_news_tab = VALID_NEWS_TABS[0]

NewsTabType = Annotated[
    str,
    typer.Option(
        callback=lambda x: (
            x
            if x in VALID_NEWS_TABS
            else raise_exception(typer.BadParameter(f"Invalid news tab: {x}"))
        ),
        help=f"Tab of the news ({', '.join(VALID_NEWS_TABS)})",
    ),
]

SECTOR_KEYS = [
    "basic-materials",
    "communication-services",
    "consumer-cyclical",
    "consumer-defensive",
    "energy",
    "financial-services",
    "healthcare",
    "industrials",
    "real-estate",
    "technology",
    "utilities",
]

SectorKeyType = Annotated[
    str,
    typer.Argument(
        callback=lambda x: (
            x
            if x in SECTOR_KEYS
            else raise_exception(typer.BadParameter(f"Invalid sector key: {x}"))
        ),
        help=f"Sector key ({', '.join(SECTOR_KEYS)})",
    ),
]

IndustryKeyType = Annotated[
    str,
    typer.Argument(
        help="Industry key",
    ),
]
