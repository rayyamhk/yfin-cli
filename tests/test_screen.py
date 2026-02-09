"""Tests for the screen command parsing functions."""

import pytest
import typer
import yfinance as yf
from src.commands.screen import parse_filter, parse_json_query


class TestParseFilter:
    """Tests for the parse_filter function."""

    def test_parse_filter_eq_operator(self):
        """Test parsing a filter with 'eq' operator."""
        result = parse_filter("sector eq Technology")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_gt_operator(self):
        """Test parsing a filter with 'gt' operator."""
        result = parse_filter("intradaymarketcap gt 1000000000")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_gte_operator(self):
        """Test parsing a filter with 'gte' operator."""
        result = parse_filter("beta gte 1")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_lt_operator(self):
        """Test parsing a filter with 'lt' operator."""
        result = parse_filter("beta lt 2")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_lte_operator(self):
        """Test parsing a filter with 'lte' operator."""
        result = parse_filter("avgdailyvol3m lte 1000000")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_btwn_operator(self):
        """Test parsing a filter with 'btwn' operator."""
        result = parse_filter("beta btwn 0.5,1.5")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_is_in_operator(self):
        """Test parsing a filter with 'is-in' operator for comma-separated values."""
        result = parse_filter("exchange is-in NYQ,NMS")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_case_insensitive_field(self):
        """Test that field names are case-insensitive."""
        result = parse_filter("SECTOR eq Technology")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_case_insensitive_operator(self):
        """Test that operators are case-insensitive."""
        result = parse_filter("sector EQ Technology")
        assert isinstance(result, yf.EquityQuery)

    def test_parse_filter_invalid_format_missing_value(self):
        """Test parsing a filter with missing value."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_filter("sector eq")
        assert "Invalid filter format" in str(exc_info.value)

    def test_parse_filter_invalid_format_missing_operator(self):
        """Test parsing a filter with missing operator."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_filter("sector Technology")
        assert "Invalid filter format" in str(exc_info.value)

    def test_parse_filter_invalid_field(self):
        """Test parsing a filter with invalid field."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_filter("invalidField eq value")
        assert "Invalid field" in str(exc_info.value)

    def test_parse_filter_invalid_operator(self):
        """Test parsing a filter with invalid operator."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_filter("sector invalidOp Technology")
        assert "Invalid operator" in str(exc_info.value)

    def test_parse_filter_invalid_numeric_value(self):
        """Test parsing a filter with non-numeric value for numeric field."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_filter("beta gt abc")
        assert "Expected a number" in str(exc_info.value)

    def test_parse_filter_invalid_enum_value(self):
        """Test parsing a filter with invalid enum value."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_filter("sector eq InvalidSector")
        assert "Invalid value" in str(exc_info.value)

    def test_parse_filter_whitespace_handling(self):
        """Test that extra whitespace is handled correctly."""
        result = parse_filter("  sector   eq   Technology  ")
        assert isinstance(result, yf.EquityQuery)


class TestParseJsonQuery:
    """Tests for the parse_json_query function."""

    def test_parse_json_query_simple_filter_string(self):
        """Test parsing a JSON query that is just a filter string."""
        result = parse_json_query('"sector eq Technology"')
        assert isinstance(result, yf.EquityQuery)

    def test_parse_json_query_and_operator(self):
        """Test parsing a JSON query with 'and' operator."""
        json_str = '{"operator": "and", "queries": ["sector eq Technology", "beta gt 1"]}'
        result = parse_json_query(json_str)
        assert isinstance(result, yf.EquityQuery)

    def test_parse_json_query_or_operator(self):
        """Test parsing a JSON query with 'or' operator."""
        json_str = '{"operator": "or", "queries": ["sector eq Technology", "sector eq Healthcare"]}'
        result = parse_json_query(json_str)
        assert isinstance(result, yf.EquityQuery)

    def test_parse_json_query_nested(self):
        """Test parsing a nested JSON query."""
        json_str = '''{
            "operator": "and",
            "queries": [
                "beta gt 1",
                {
                    "operator": "or",
                    "queries": ["sector eq Technology", "sector eq Healthcare"]
                }
            ]
        }'''
        result = parse_json_query(json_str)
        assert isinstance(result, yf.EquityQuery)

    def test_parse_json_query_single_operand_unwrap(self):
        """Test that single operand queries are unwrapped."""
        json_str = '{"operator": "and", "queries": ["sector eq Technology"]}'
        result = parse_json_query(json_str)
        # Should unwrap since there's only one operand
        assert isinstance(result, yf.EquityQuery)

    def test_parse_json_query_invalid_json(self):
        """Test parsing invalid JSON."""
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query("not valid json")
        assert "Invalid JSON query" in str(exc_info.value)

    def test_parse_json_query_missing_operator(self):
        """Test parsing JSON query with missing 'operator' key."""
        json_str = '{"queries": ["sector eq Technology"]}'
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query(json_str)
        assert "'operator' is required" in str(exc_info.value)

    def test_parse_json_query_missing_queries(self):
        """Test parsing JSON query with missing 'queries' key."""
        json_str = '{"operator": "and"}'
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query(json_str)
        assert "'queries' is required" in str(exc_info.value)

    def test_parse_json_query_invalid_operator(self):
        """Test parsing JSON query with invalid operator."""
        json_str = '{"operator": "xor", "queries": ["sector eq Technology"]}'
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query(json_str)
        assert "'operator' must be either 'and' or 'or'" in str(exc_info.value)

    def test_parse_json_query_empty_queries(self):
        """Test parsing JSON query with empty queries array."""
        json_str = '{"operator": "and", "queries": []}'
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query(json_str)
        assert "'queries' must be a non-empty list" in str(exc_info.value)

    def test_parse_json_query_invalid_node_type(self):
        """Test parsing JSON query with invalid node type."""
        json_str = "123"
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query(json_str)
        assert "unexpected type" in str(exc_info.value)

    def test_parse_json_query_invalid_filter_in_queries(self):
        """Test parsing JSON query with invalid filter inside queries."""
        json_str = '{"operator": "and", "queries": ["invalidField eq value"]}'
        with pytest.raises(typer.BadParameter) as exc_info:
            parse_json_query(json_str)
        assert "Invalid field" in str(exc_info.value)
