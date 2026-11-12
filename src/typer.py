import typer
from typing import Annotated
from .utils import (
    get_today_date_string,
    validate_date_string,
    validate_value_in_list,
)

TickerType = Annotated[
    str,
    typer.Argument(
        help="Stock ticker symbol (e.g., TSLA, AAPL)", callback=lambda x: x.upper()
    ),
]

VALID_OUTPUT_TYPES = ["json", "table"]

default_output = VALID_OUTPUT_TYPES[0]

OutputType = Annotated[
    str,
    typer.Option(
        callback=validate_value_in_list(VALID_OUTPUT_TYPES),
        help=f"Output format ({', '.join(VALID_OUTPUT_TYPES)})",
    ),
]

default_frequency = "yearly"

FrequencyType = Annotated[
    str,
    typer.Option(
        callback=validate_value_in_list(["yearly", "quarterly"]),
        help="Frequency of the data (yearly, quarterly)",
    ),
]

ExtendedFrequencyType = Annotated[
    str,
    typer.Option(
        callback=validate_value_in_list(["yearly", "quarterly", "trailing"]),
        help="Frequency of the data (yearly, quarterly, trailing)",
    ),
]

StartDateType = Annotated[
    str,
    typer.Option(
        default_factory=get_today_date_string,
        callback=validate_date_string,
        help="Start date (YYYY-MM-DD), default today",
    ),
]

StartDateTypeOptional = Annotated[
    str | None,
    typer.Option(
        callback=lambda x: validate_date_string(x) if x else None,
        help="Start date (YYYY-MM-DD)",
    ),
]

EndDateType = Annotated[
    str | None,
    typer.Option(
        callback=lambda x: validate_date_string(x) if x else None,
        help="End date (YYYY-MM-DD), default 7 days from start",
    ),
]

EndDateTypeOptional = Annotated[
    str | None,
    typer.Option(
        callback=lambda x: validate_date_string(x) if x else None,
        help="End date (YYYY-MM-DD)",
    ),
]

VALID_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

default_period = VALID_PERIODS[-1]  # max


PeriodType = Annotated[
    str,
    typer.Option(
        callback=validate_value_in_list(VALID_PERIODS),
        help=f"Data period {', '.join(VALID_PERIODS)}",
    ),
]

PeriodTypeOptional = Annotated[
    str | None,
    typer.Option(
        callback=lambda x: validate_value_in_list(VALID_PERIODS)(x) if x else None,
        help=f"Data period {', '.join(VALID_PERIODS)}",
    ),
]

default_limit = 12

LimitType = Annotated[
    int,
    typer.Option(
        help="Maximum number of results to show",
    ),
]

# yfinance's earnings-dates scraper rejects limits outside 1-100.
EarningsDatesLimitType = Annotated[
    int,
    typer.Option(
        "--limit",
        min=1,
        max=100,
        help="Maximum number of results to show (1-100)",
    ),
]

default_offset = 0

# Default row limit for long, newest-first histories (analyst actions, filings,
# insider transactions), which otherwise return years of rows.
default_recent_limit = 20

RecentLimitType = Annotated[
    int,
    typer.Option(
        "--limit",
        help="Maximum number of rows, newest first (0 for all)",
    ),
]

OffsetType = Annotated[
    int,
    typer.Option(
        help="Offset of the results",
    ),
]

default_market_cap = None

MarketCapType = Annotated[
    int | None,
    typer.Option(
        help="Minimum market cap filter, e.g. 10000000000 for $10B (default: no filter)",
    ),
]

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

default_interval = VALID_INTERVALS[8]  # "1d"

IntervalType = Annotated[
    str,
    typer.Option(
        callback=validate_value_in_list(VALID_INTERVALS),
        help=f"Data interval ({', '.join(VALID_INTERVALS)})",
    ),
]

default_count = 10

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
        callback=validate_value_in_list(["all", "news", "press releases"]),
        help="Tab of the news (all, news, press releases)",
    ),
]

SectorKeyType = Annotated[
    str,
    typer.Argument(
        help="A valid sector key, can be found using `yfin sector-keys`",
    ),
]

IndustryKeyType = Annotated[
    str,
    typer.Argument(
        help="A valid industry key, can be found using `yfin sector-industries <sector-key>`",
    ),
]

ScreenFilterTypeOptional = Annotated[
    list[str] | None,
    typer.Option(
        "--filter",  # parameter name is plural
        help="Filter in '<field> <operator> <value>' format (e.g., 'sector eq Technology')",
    ),
]

ScreenPredefinedQueryTypeOptional = Annotated[
    str | None,
    typer.Option(
        help="Predefined query, can be found using `yfin screen-predefined-queries`",
    ),
]

ScreenJsonQueryTypeOptional = Annotated[
    str | None,
    typer.Option(
        help="Complex query in JSON format: {'operator': 'and|or', 'queries': [<filter1>, <filter2>, <json_query>, ...]}.",
    ),
]

ScreenQueryFieldType = Annotated[
    str | None,
    typer.Option(
        help="Query field, can be found using `yfin screen-query-fields`",
    ),
]

default_sort_order = "desc"

ScreenSortOrderType = Annotated[
    str,
    typer.Option(
        callback=validate_value_in_list(["asc", "desc"]),
        help="Sort order, can be 'asc' or 'desc'",
    ),
]

ScreenResultFieldsType = Annotated[
    str | None,
    typer.Option(
        "--fields",
        help="Comma-separated result fields to return, e.g. 'symbol,trailingPE,marketCap' (symbol is always included)",
    ),
]

ScreenAllFieldsType = Annotated[
    bool,
    typer.Option(
        "--all-fields",
        help="Return every field Yahoo provides (~90 per result) instead of the default summary",
    ),
]
