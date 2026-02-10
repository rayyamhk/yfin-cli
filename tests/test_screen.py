"""Tests for the screen command parsing functions."""

import pytest
import typer
import yfinance as yf
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
        "exchange is-in NYQ,NMS",
    ],
    ids=["gt", "gte", "lt", "lte", "btwn", "is_in"],
)
def test_parse_filter_valid_operators(filter_str):
    result = parse_filter(filter_str)
    assert isinstance(result, yf.EquityQuery)


@pytest.mark.parametrize(
    "filter_str, error_fragment",
    [
        ("sector eq", "Invalid filter format"),
        ("sector Technology", "Invalid filter format"),
        ("invalidField eq value", "Invalid field"),
        ("sector invalidOp Technology", "Invalid operator"),
        ("beta gt abc", "Expected a number"),
        ("sector eq InvalidSector", "Invalid value"),
    ],
    ids=[
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
