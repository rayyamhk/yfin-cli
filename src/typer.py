import typer
from datetime import datetime
from typing import Annotated
from .validator import (
    validate_date_string,
    validate_output_type,
    validate_frequency,
    validate_extended_frequency,
    validate_interval,
    validate_news_tab,
)
from .formatter import format_datetime
from .utils import increment_datetime_by_days

TickerType = Annotated[
    str,
    typer.Argument(
        help="Stock ticker symbol (e.g., TSLA, AAPL)", callback=lambda x: x.upper()
    ),
]

default_output = "table"

OutputType = Annotated[
    str,
    typer.Option(callback=validate_output_type, help="Output format (table)"),
]

default_frequency = "yearly"

FrequencyType = Annotated[
    str,
    typer.Option(
        callback=validate_frequency,
        help="Frequency of the data (yearly or quarterly)",
    ),
]

ExtendedFrequencyType = Annotated[
    str,
    typer.Option(
        callback=validate_extended_frequency,
        help="Frequency of the data (yearly, quarterly or trailing)",
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

IntervalType = Annotated[
    str,
    typer.Option(
        callback=validate_interval,
        help="Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)",
    ),
]

default_count = 5

CountType = Annotated[
    int,
    typer.Option(
        help="Number of results to show",
    ),
]

default_news_tab = "all"

NewsTabType = Annotated[
    str,
    typer.Option(
        callback=validate_news_tab,
        help="Tab of the news (all, news, press releases)",
    ),
]
