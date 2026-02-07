"""Tests for the cashflow command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from src.cli import app

runner = CliRunner()


# Mock Cash Flow data for testing
def create_mock_cashflow_data(freq="yearly"):
    """Create a mock pandas DataFrame similar to yf.Ticker.get_cashflow output."""
    dates = [
        pd.Timestamp("2025-06-30"),
        pd.Timestamp("2024-06-30"),
        pd.Timestamp("2023-06-30"),
    ]
    if freq == "quarterly":
        dates = [
            pd.Timestamp("2025-06-30"),
            pd.Timestamp("2025-03-31"),
            pd.Timestamp("2024-12-31"),
        ]
    elif freq == "trailing":
        # yfinance might return NaT or TTM string for trailing?
        # Let's assume NaT or current date for TTM column usually
        dates = [pd.NaT]

    data = {
        dates[0]: [5000.0, -2000.0],
    }
    # Add more columns for non-trailing
    if freq != "trailing":
        data[dates[1]] = [4000.0, -1500.0]
        data[dates[2]] = [3000.0, -1000.0]

    index = ["OperatingCashFlow", "CapitalExpenditure"]
    return pd.DataFrame(data, index=index)


class TestCashFlowCommand:
    """Tests for the cashflow CLI command."""

    @patch("src.commands.cashflow.yf.Ticker")
    def test_cashflow_basic(self, mock_ticker):
        """Test basic cashflow command execution (yearly)."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_cashflow.return_value = create_mock_cashflow_data(
            freq="yearly"
        )

        result = runner.invoke(app, ["cashflow", "MSFT"])

        assert result.exit_code == 0
        assert "OperatingCashFlow" in result.output
        assert "5.00K" in result.output

        # Verify call args
        mock_instance.get_cashflow.assert_called_with(pretty=True, freq="yearly")

    @patch("src.commands.cashflow.yf.Ticker")
    def test_cashflow_quarterly(self, mock_ticker):
        """Test cashflow command with --frequency quarterly."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_cashflow.return_value = create_mock_cashflow_data(
            freq="quarterly"
        )

        result = runner.invoke(app, ["cashflow", "MSFT", "--frequency", "quarterly"])

        assert result.exit_code == 0
        assert "2025-03-31" in result.output

        # Verify call args
        mock_instance.get_cashflow.assert_called_with(pretty=True, freq="quarterly")

    @patch("src.commands.cashflow.yf.Ticker")
    def test_cashflow_trailing(self, mock_ticker):
        """Test cashflow command with --frequency trailing."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_cashflow.return_value = create_mock_cashflow_data(
            freq="trailing"
        )

        result = runner.invoke(app, ["cashflow", "MSFT", "--frequency", "trailing"])

        assert result.exit_code == 0

        # Verify call args
        mock_instance.get_cashflow.assert_called_with(pretty=True, freq="trailing")

    @patch("src.commands.cashflow.yf.Ticker")
    def test_cashflow_no_data(self, mock_ticker):
        """Test cashflow command when no data is found."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_cashflow.return_value = pd.DataFrame()

        result = runner.invoke(app, ["cashflow", "MSFT"])

        # Typer exit code 1 raised explicitly
        assert result.exit_code == 1
        assert "No cash flow statement found" in result.output

    @patch("src.commands.cashflow.yf.Ticker")
    def test_cashflow_api_error(self, mock_ticker):
        """Test cashflow command handles API errors."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_cashflow.side_effect = Exception("API Error")

        result = runner.invoke(app, ["cashflow", "MSFT"])

        assert result.exit_code == 1
        assert "Unexpected error" in result.output
