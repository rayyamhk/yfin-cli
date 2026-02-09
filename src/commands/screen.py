import yfinance as yf
import typer
import json
from ..decorators import handle_errors, with_output
from ..typer import (
    ScreenFilterType,
    ScreenPredefinedQueryType,
    ScreenJsonQueryType,
    OffsetType,
    default_offset,
    LimitType,
    default_limit,
    ScreenQueryFieldType,
    ScreenSortOrderType,
    default_sort_order,
)
from ..utils import is_number, count_specified

VALID_FIELDS_DICT = yf.const.EQUITY_SCREENER_FIELDS
VALID_VALUES_DICT = yf.const.EQUITY_SCREENER_EQ_MAP
VALID_FIELDS = set().union(*VALID_FIELDS_DICT.values())
VALID_REGIONS = set(VALID_VALUES_DICT.get("region"))
VALID_EXCHANGES = set().union(*VALID_VALUES_DICT.get("exchange").values())
VALID_SECTORS = set(VALID_VALUES_DICT.get("sector"))
VALID_INDUSTRIES = set().union(*VALID_VALUES_DICT.get("industry").values())
VALID_PEER_GROUPS = set(VALID_VALUES_DICT.get("peer_group"))
PREDEFINED_QUERIES = set(yf.PREDEFINED_SCREENER_QUERIES.keys())
VALID_OPERATORS = {
    "eq",
    "gt",
    "gte",
    "lt",
    "lte",
    "btwn",
    "is-in",
}


@handle_errors
@with_output
def screen_query_fields():
    """Get a list of all valid fields for screening."""
    return [{"field": f} for f in sorted(list(VALID_FIELDS))]


@handle_errors
@with_output
def screen_query_values(field: ScreenQueryFieldType):
    """Get a list of all valid values for a field."""
    if field == "region":
        values = list(VALID_REGIONS)
    elif field == "exchange":
        values = list(VALID_EXCHANGES)
    elif field == "sector":
        values = list(VALID_SECTORS)
    elif field == "industry":
        values = list(VALID_INDUSTRIES)
    elif field == "peer_group":
        values = list(VALID_PEER_GROUPS)
    else:
        values = []

    return [{"value": v} for v in sorted(values)]


@handle_errors
@with_output
def screen_predefined_queries():
    """Get a list of all valid predefined queries."""
    return [{"query": q} for q in sorted(list(PREDEFINED_QUERIES))]


def validate_field(field: str):
    """
    Validate the field.
    """
    if field not in VALID_FIELDS:
        raise typer.BadParameter(
            f"Invalid field: '{field}'. Valid fields can be found using `yfin screen-query-fields`."
        )


def parse_value(field: str, value: str) -> str | float:
    """
    Validate the value against the field, then return it into the correct type.
    """
    if field in VALID_FIELDS_DICT.get("eq_fields"):
        # fields in `eq_fields` should operate with fixed values
        if field not in ["region", "exchange", "sector", "industry", "peer_group"]:
            # This should never happen
            raise ValueError(f"Invalid field '{field}' for eq_fields")

        if field == "region" and value not in VALID_REGIONS:
            raise typer.BadParameter(
                f"Invalid value: '{value}' for 'region' field. Valid values can be found using `yfin screen-query-values region`."
            )
        elif field == "exchange" and value not in VALID_EXCHANGES:
            raise typer.BadParameter(
                f"Invalid value: '{value}' for 'exchange' field. Valid values can be found using `yfin screen-query-values exchange`."
            )
        elif field == "sector" and value not in VALID_SECTORS:
            raise typer.BadParameter(
                f"Invalid value: '{value}' for 'sector' field. Valid values can be found using `yfin screen-query-values sector`."
            )
        elif field == "industry" and value not in VALID_INDUSTRIES:
            raise typer.BadParameter(
                f"Invalid value: '{value}' for 'industry' field. Valid values can be found using `yfin screen-query-values industry`."
            )
        elif field == "peer_group" and value not in VALID_PEER_GROUPS:
            raise typer.BadParameter(
                f"Invalid value: '{value}' for 'peer_group' field. Valid values can be found using `yfin screen-query-values peer_group`."
            )
        return value

    # Remaining fields are numeric
    if not is_number(value):
        raise typer.BadParameter(
            f"Invalid value: '{value}' for '{field}' field. Expected a number."
        )
    return float(value)


def parse_filter(filter_str: str) -> yf.EquityQuery:
    """
    Parse a filter string like '<field> <operator> <value>' into an EquityQuery.
    Example: 'sector eq Technology' -> EquityQuery('eq', ['sector', 'Technology'])
    """
    parts = filter_str.strip().split(maxsplit=2)
    if len(parts) != 3:
        raise typer.BadParameter(
            f"Invalid filter format: '{filter_str}'. Expected '<field> <operator> <value>'."
        )

    field, operator, value = (parts[0].lower(), parts[1].lower(), parts[2])

    validate_field(field)

    if operator not in VALID_OPERATORS:
        raise typer.BadParameter(
            f"Invalid operator: '{operator}'. Use one of {', '.join(sorted(list(VALID_OPERATORS)))}"
        )

    if operator in ["is-in", "btwn"]:
        # comma-separated values
        values = [parse_value(field, v.strip()) for v in value.split(",")]
        if operator == "btwn" and len(values) != 2:
            raise typer.BadParameter(
                f"Invalid value: '{value}' for '{field}' field. Expected exactly two values."
            )
    else:
        values = [parse_value(field, value)]

    return yf.EquityQuery(operator, [field] + values)


def parse_json_query(json_query: str) -> yf.EquityQuery:
    """
    Parse a JSON query into an EquityQuery.
    """
    try:
        query_node = json.loads(json_query)
    except json.JSONDecodeError:
        raise typer.BadParameter(f"Invalid JSON query: '{json_query}'.")

    def _build_query(node):
        if isinstance(node, str):
            return parse_filter(node)

        if isinstance(node, dict):
            operator = node.get("operator")
            queries = node.get("queries")
            if operator is None:
                raise typer.BadParameter("Invalid query, 'operator' is required.")

            if queries is None:
                raise typer.BadParameter("Invalid query, 'queries' is required.")

            if operator not in ["and", "or"]:
                raise typer.BadParameter(
                    "Invalid query, 'operator' must be either 'and' or 'or'."
                )

            if not isinstance(queries, list) or len(queries) == 0:
                raise typer.BadParameter(
                    "Invalid query, 'queries' must be a non-empty list."
                )
            operands = [_build_query(q) for q in queries]

            # yfinance does not support single operand queries
            if len(operands) == 1:
                return operands[0]

            return yf.EquityQuery(operator, operands)

        raise typer.BadParameter(
            f"Invalid query, unexpected type: {type(node).__name__}"
        )

    return _build_query(query_node)


@handle_errors
@with_output
def screen(
    filters: ScreenFilterType = None,
    predefined: ScreenPredefinedQueryType = None,
    json_query: ScreenJsonQueryType = None,
    offset: OffsetType = default_offset,
    limit: LimitType = default_limit,
    sort_field: ScreenQueryFieldType = None,
    sort_order: ScreenSortOrderType = default_sort_order,
):
    """
    Run a stock screener.

    Supports predefined queries, simple filters (implicitly ANDed), or complex JSON queries.
    Options --predefined, --filter, and --json-query are mutually exclusive.
    """
    specified_count = count_specified(filters, predefined, json_query)
    if specified_count != 1:
        raise typer.BadParameter(
            "Exactly one of --filter, --predefined, or --json-query must be specified."
        )

    if predefined:
        if predefined not in PREDEFINED_QUERIES:
            raise typer.BadParameter(
                f"Invalid predefined query: '{predefined}'. Valid predefined queries can be found using `yfin screen-predefined-queries`."
            )
        final_query = predefined
    elif filters:
        queries = [parse_filter(f) for f in filters]
        final_query = (
            queries[0] if len(queries) == 1 else yf.EquityQuery("and", queries)
        )
    else:
        final_query = parse_json_query(json_query)

    if sort_field:
        validate_field(sort_field)

    # yfinance docs say that size is only for custom queries, count is only for predefined queries
    if predefined:
        response = yf.screen(
            final_query,
            offset=offset,
            count=limit,
            sortField=sort_field,
            sortAsc=sort_order == "asc",
        )
    else:
        response = yf.screen(
            final_query,
            offset=offset,
            size=limit,
            sortField=sort_field,
            sortAsc=sort_order == "asc",
        )

    return response["quotes"]
