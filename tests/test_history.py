"""Tests for the history command."""

import pytest
import typer
import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch
from src.cli import app

runner = CliRunner()


# Mock DataFrame for testing
def create_mock_history_data():
    """Create a mock pandas DataFrame similar to yfinance history output."""
    data = {
        "Open": [100.0, 102.0],
        "High": [105.0, 108.0],
        "Low": [99.0, 101.0],
        "Close": [104.0, 107.0],
        "Volume": [1000000, 1200000],
    }
    index = pd.DatetimeIndex(["2026-02-05", "2026-02-06"])
    return pd.DataFrame(data, index=index)


class TestHistoryCommand:
    """Tests for the history CLI command."""

    @patch("src.commands.history.yf.Ticker")
    def test_history_basic(self, mock_ticker):
        """Test basic history command execution."""
        mock_ticker.return_value.history.return_value = create_mock_history_data()
        result = runner.invoke(app, ["history", "TSLA"])
        assert result.exit_code == 0
        assert "104.0" in result.stdout  # Close price (raw value)

    @patch("src.commands.history.yf.Ticker")
    def test_history_with_interval(self, mock_ticker):
        """Test history command with --interval option."""
        mock_ticker.return_value.history.return_value = create_mock_history_data()
        result = runner.invoke(app, ["history", "TSLA", "--interval", "1h"])
        assert result.exit_code == 0
        mock_ticker.return_value.history.assert_called_once()
        call_kwargs = mock_ticker.return_value.history.call_args[1]
        assert call_kwargs["interval"] == "1h"

    @patch("src.commands.history.yf.Ticker")
    def test_history_with_period(self, mock_ticker):
        """Test history command with --period option."""
        mock_ticker.return_value.history.return_value = create_mock_history_data()
        result = runner.invoke(app, ["history", "TSLA", "--period", "5d"])
        assert result.exit_code == 0
        call_kwargs = mock_ticker.return_value.history.call_args[1]
        assert call_kwargs["period"] == "5d"

    @patch("src.commands.history.yf.Ticker")
    def test_history_with_start_end(self, mock_ticker):
        """Test history command with --start and --end options."""
        mock_ticker.return_value.history.return_value = create_mock_history_data()
        result = runner.invoke(
            app, ["history", "TSLA", "--start", "2026-01-01", "--end", "2026-02-01"]
        )
        assert result.exit_code == 0
        call_kwargs = mock_ticker.return_value.history.call_args[1]
        assert call_kwargs["start"] == "2026-01-01"
        assert call_kwargs["end"] == "2026-02-01"

    def test_history_invalid_interval(self):
        """Test history command with invalid interval option."""
        result = runner.invoke(app, ["history", "TSLA", "--interval", "invalid"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_history_invalid_period(self):
        """Test history command with invalid period option."""
        result = runner.invoke(app, ["history", "TSLA", "--period", "invalid"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_history_invalid_date_format(self):
        """Test history command with invalid date format."""
        result = runner.invoke(app, ["history", "TSLA", "--start", "01-01-2026"])
        assert result.exit_code == 2
        assert "Invalid date format" in result.output

    def test_history_too_many_options(self):
        """Test history command with too many time options."""
        result = runner.invoke(
            app,
            [
                "history",
                "TSLA",
                "--period",
                "1mo",
                "--start",
                "2026-01-01",
                "--end",
                "2026-02-01",
            ],
        )
        # Typer returns exit code 2 for BadParameter, message may be in stdout or output
        assert result.exit_code != 0
        output = result.stdout + (result.output or "")
        assert "At most 2" in output or result.exit_code == 2

    @patch("src.commands.history.yf.Ticker")
    def test_history_no_data(self, mock_ticker):
        """Test history command when no data is found."""
        mock_ticker.return_value.history.return_value = pd.DataFrame()
        result = runner.invoke(app, ["history", "TSLA"])
        assert result.exit_code == 1
        assert "No data found" in result.output

    @patch("src.commands.history.yf.Ticker")
    def test_history_ticker_uppercase(self, mock_ticker):
        """Test that ticker is converted to uppercase."""
        mock_ticker.return_value.history.return_value = create_mock_history_data()
        runner.invoke(app, ["history", "tsla"])
        mock_ticker.assert_called_once_with("TSLA")

    @patch("src.commands.history.yf.Ticker")
    def test_history_api_error(self, mock_ticker):
        """Test history command handles API errors gracefully."""
        mock_ticker.return_value.history.side_effect = Exception("API Error")
        result = runner.invoke(app, ["history", "TSLA"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output

    @patch("src.commands.history.yf.Ticker")
    def test_history_default_period(self, mock_ticker):
        """Test that default period is 1mo when no time options specified."""
        mock_ticker.return_value.history.return_value = create_mock_history_data()
        runner.invoke(app, ["history", "TSLA"])
        call_kwargs = mock_ticker.return_value.history.call_args[1]
        assert call_kwargs["period"] == "1mo"

