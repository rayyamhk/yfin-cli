"""Tests for WriterFactory, JsonWriter, and TableWriter."""

import json
import pytest
from src.writer import WriterFactory, JsonWriter, TableWriter
from unittest.mock import patch


# ── WriterFactory ─────────────────────────────────────────────────────


def test_factory_json():
    assert isinstance(WriterFactory.get_writer("json"), JsonWriter)


def test_factory_table():
    assert isinstance(WriterFactory.get_writer("table"), TableWriter)


def test_factory_invalid():
    with pytest.raises(ValueError, match="Unsupported writer type"):
        WriterFactory.get_writer("csv")


# ── TableWriter (dict input) ─────────────────────────────────────────


def test_table_writer_dict(capsys):
    writer = TableWriter()
    writer.write({"name": "AAPL", "price": 150})
    output = capsys.readouterr().out

    assert "name" in output
    assert "price" in output
    assert "AAPL" in output
    assert "150" in output


def test_table_writer_dict_single_key(capsys):
    writer = TableWriter()
    writer.write({"status": "open"})
    output = capsys.readouterr().out

    assert "status" in output
    assert "open" in output


# ── TableWriter (list input) ─────────────────────────────────────────


def test_table_writer_list(capsys):
    writer = TableWriter()
    writer.write(
        [
            {"name": "AAPL", "price": 150},
            {"name": "TSLA", "price": 400},
        ]
    )
    output = capsys.readouterr().out

    assert "name" in output
    assert "price" in output
    assert "AAPL" in output
    assert "TSLA" in output
    assert "150" in output
    assert "400" in output


def test_table_writer_empty_list(capsys):
    writer = TableWriter()
    writer.write([])
    output = capsys.readouterr().out

    # Should not crash, just print an empty table
    assert output is not None


# ── JsonWriter ────────────────────────────────────────────────────────


def test_json_writer_dict(capsys):
    writer = JsonWriter()
    writer.write({"key": "value"})
    output = capsys.readouterr().out
    data = json.loads(output)

    assert data == {"key": "value"}


def test_json_writer_list(capsys):
    writer = JsonWriter()
    writer.write([{"a": 1}, {"a": 2}])
    output = capsys.readouterr().out
    data = json.loads(output)

    assert data == [{"a": 1}, {"a": 2}]


# ── --output table CLI integration ────────────────────────────────────


@patch("src.commands.market.yf.Market")
def test_cli_output_table(mock_market, invoke):
    """--output table should render a Rich table with the data."""
    mock_market.return_value.status = {
        "market_state": "REGULAR",
        "exchange": "NMS",
    }
    result = invoke("--output", "table", "market-status")

    assert result.exit_code == 0
    assert "market_state" in result.output
    assert "REGULAR" in result.output
    assert "exchange" in result.output
    assert "NMS" in result.output


@patch("src.commands.market.yf.Market")
def test_cli_output_json_default(mock_market, invoke_json):
    """Default --output json should still work."""
    mock_market.return_value.status = {"market_state": "REGULAR"}
    code, data = invoke_json("market-status")

    assert code == 0
    assert data["market_state"] == "REGULAR"
