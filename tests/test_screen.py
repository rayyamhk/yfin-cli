"""Tests for the screen command parsing functions."""

import pytest
import typer
import yfinance as yf
from unittest.mock import patch
from src.commands import screen as screen_cmd
from src.typer import default_limit, default_offset
from src.commands.screen import parse_filter, parse_json_query


# ── parse_filter ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "filter_str",
    [
        "sector eq Technology",
        "SECTOR eq Technology",  # case-insensitive field
        "sector EQ Technology",  # case-insensitive operator
        "  sector   eq   Technology  ",  # extra whitespace
    ],
    ids=["basic_eq", "case_field", "case_operator", "whitespace"],
)
def test_parse_filter_valid_eq(filter_str):
    result = parse_filter(filter_str)
    assert isinstance(result, yf.EquityQuery)


@pytest.mark.parametrize(
    "filter_str",
    [
        "intradaymarketcap gt 1000000000",
        "beta gte 1",
        "beta lt 2",
        "avgdailyvol3m lte 1000000",
        "beta btwn 0.5,1.5",
        "beta btwn 0.5,      1.5  ",
        "exchange is-in NYQ,NMS,CXI",
        "exchange is-in NYQ,    NMS ,   CXI ",
    ],
    ids=[
        "gt",
        "gte",
        "lt",
        "lte",
        "btwn",
        "btwn_whitespace",
        "is_in",
        "is_in_whitespace",
    ],
)
def test_parse_filter_valid_operators(filter_str):
    result = parse_filter(filter_str)
    assert isinstance(result, yf.EquityQuery)


@pytest.mark.parametrize(
    "filter_str, error_fragment",
    [
        {"sector", "Invalid filter format"},
        ("sector eq", "Invalid filter format"),
        ("sector Technology", "Invalid filter format"),
        ("invalidField eq value", "Invalid field"),
        ("sector invalidOp Technology", "Invalid operator"),
        ("beta gt abc", "Expected a number"),
        ("sector eq InvalidSector", "Invalid value"),
    ],
    ids=[
        "missing_operator",
        "missing_value",
        "missing_operator",
        "invalid_field",
        "invalid_operator",
        "non_numeric_value",
        "invalid_enum_value",
    ],
)
def test_parse_filter_invalid(filter_str, error_fragment):
    with pytest.raises(typer.BadParameter) as exc_info:
        parse_filter(filter_str)
    assert error_fragment in str(exc_info.value)


# ── parse_json_query ──────────────────────────────────────────────────


@pytest.mark.parametrize(
    "json_str",
    [
        '"sector eq Technology"',
        '{"operator": "and", "queries": ["sector eq Technology", "beta gt 1"]}',
        '{"operator": "or", "queries": ["sector eq Technology", "sector eq Healthcare"]}',
        '{"operator": "and", "queries": ["sector eq Technology"]}',  # single-operand unwrap
    ],
    ids=["simple_string", "and_operator", "or_operator", "single_operand"],
)
def test_parse_json_query_valid(json_str):
    result = parse_json_query(json_str)
    assert isinstance(result, yf.EquityQuery)


def test_parse_json_query_nested():
    json_str = """{
        "operator": "and",
        "queries": [
            "beta gt 1",
            {
                "operator": "or",
                "queries": ["sector eq Technology", "sector eq Healthcare"]
            }
        ]
    }"""
    result = parse_json_query(json_str)
    assert isinstance(result, yf.EquityQuery)


@pytest.mark.parametrize(
    "json_str, error_fragment",
    [
        ("not valid json", "Invalid JSON query"),
        ('{"queries": ["sector eq Technology"]}', "'operator' is required"),
        ('{"operator": "and"}', "'queries' is required"),
        (
            '{"operator": "xor", "queries": ["sector eq Technology"]}',
            "'operator' must be either 'and' or 'or'",
        ),
        ('{"operator": "and", "queries": []}', "'queries' must be a non-empty list"),
        ("123", "unexpected type"),
        ('{"operator": "and", "queries": ["invalidField eq value"]}', "Invalid field"),
    ],
    ids=[
        "invalid_json",
        "missing_operator",
        "missing_queries",
        "invalid_operator",
        "empty_queries",
        "invalid_node_type",
        "invalid_filter_in_queries",
    ],
)
def test_parse_json_query_invalid(json_str, error_fragment):
    with pytest.raises(typer.BadParameter) as exc_info:
        parse_json_query(json_str)
    assert error_fragment in str(exc_info.value)


def test_screen_query_values_invalid_field(invoke):
    """Test that screen-query-values returns a warning for an invalid field."""
    result = invoke("screen-query-values", "--field", "invalid_field")
    assert result.exit_code == 2
    assert "Invalid field" in result.output


def test_screen_query_values_field_with_no_fixed_values(invoke):
    """Test that screen-query-values returns a warning for a valid field with no fixed values."""
    result = invoke("screen-query-values", "--field", "invalid_field")
    assert result.exit_code == 2
    assert "Invalid field" in result.output


def test_screen_query_values_valid_field_with_fixed_values(invoke):
    result = invoke("screen-query-values", "--field", "sector")
    assert result.exit_code == 0
    assert '"value": "Technology"' in result.output


# ── screen command ────────────────────────────────────────────────────


def _pick_predefined_query():
    if not screen_cmd.PREDEFINED_QUERIES:
        pytest.skip("No predefined queries available in yfinance")
    return sorted(screen_cmd.PREDEFINED_QUERIES)[0]


def _pick_valid_sort_field():
    if "beta" in screen_cmd.VALID_FIELDS:
        return "beta"
    return sorted(screen_cmd.VALID_FIELDS)[0]


@patch("src.commands.screen.yf.screen")
def test_screen_predefined_query_basic(mock_screen, invoke_json):
    query = _pick_predefined_query()
    mock_screen.return_value = {"quotes": [{"symbol": "AAPL"}]}
    code, data = invoke_json("screen", "--predefined", query)

    assert code == 0
    assert data[0]["symbol"] == "AAPL"

    args, kwargs = mock_screen.call_args
    assert args[0] == query
    assert kwargs["offset"] == default_offset
    assert kwargs["count"] == default_limit
    assert "size" not in kwargs
    assert kwargs["sortField"] is None
    assert kwargs["sortAsc"] is False


@patch("src.commands.screen.yf.screen")
def test_screen_filters_single(mock_screen, invoke_json):
    mock_screen.return_value = {"quotes": [{"symbol": "AAPL"}]}
    code, data = invoke_json("screen", "--filter", "sector eq Technology")

    assert code == 0
    assert data[0]["symbol"] == "AAPL"

    args, kwargs = mock_screen.call_args
    assert isinstance(args[0], yf.EquityQuery)
    assert kwargs["offset"] == default_offset
    assert kwargs["size"] == default_limit
    assert "count" not in kwargs
    assert kwargs["sortAsc"] is False


@patch("src.commands.screen.yf.screen")
def test_screen_filters_with_sorting(mock_screen, invoke_json):
    mock_screen.return_value = {"quotes": []}
    sort_field = _pick_valid_sort_field()
    code, _ = invoke_json(
        "screen",
        "--filter",
        "sector eq Technology",
        "--sort-field",
        sort_field,
        "--sort-order",
        "asc",
    )

    assert code == 0
    _, kwargs = mock_screen.call_args
    assert kwargs["sortField"] == sort_field
    assert kwargs["sortAsc"] is True


@patch("src.commands.screen.yf.screen")
def test_screen_json_query(mock_screen, invoke_json):
    mock_screen.return_value = {"quotes": [{"symbol": "AAPL"}]}
    json_query = '{"operator":"and","queries":["sector eq Technology","beta gt 1"]}'
    code, data = invoke_json("screen", "--json-query", json_query)

    assert code == 0
    assert data[0]["symbol"] == "AAPL"

    args, kwargs = mock_screen.call_args
    assert isinstance(args[0], yf.EquityQuery)
    assert kwargs["size"] == default_limit
    assert "count" not in kwargs


def test_screen_missing_query(invoke):
    result = invoke("screen")
    assert result.exit_code == 2
    assert "Exactly one of --filter, --predefined, or --json-query" in result.output


def test_screen_multiple_query_options(invoke):
    query = _pick_predefined_query()
    result = invoke(
        "screen", "--predefined", query, "--filter", "sector eq Technology"
    )
    assert result.exit_code == 2
    assert "Exactly one of --filter, --predefined, or --json-query" in result.output


def test_screen_invalid_predefined_query(invoke):
    result = invoke("screen", "--predefined", "not-a-query")
    assert result.exit_code == 2
    assert "Invalid predefined query" in result.output


def test_screen_invalid_sort_field(invoke):
    result = invoke(
        "screen",
        "--filter",
        "sector eq Technology",
        "--sort-field",
        "not_a_field",
    )
    assert result.exit_code == 2
    assert "Invalid field" in result.output
