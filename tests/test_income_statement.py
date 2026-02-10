"""Tests for the income-statement command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from src.cli import app

runner = CliRunner()


# Mock Income Statement data for testing
def create_mock_income_statement_data(freq="yearly"):
    """Create a mock pandas DataFrame similar to yf.Ticker.get_income_stmt output."""
    dates = [
        pd.Timestamp("2025-09-30"),
        pd.Timestamp("2024-09-30"),
        pd.Timestamp("2023-09-30"),
    ]
    if freq == "quarterly":
        dates = [
            pd.Timestamp("2025-12-31"),
            pd.Timestamp("2025-09-30"),
            pd.Timestamp("2025-06-30"),
        ]

    data = {
        dates[0]: [1000.0, 500.0, 50.0],
        dates[1]: [900.0, 450.0, 45.0],
        dates[2]: [800.0, 400.0, 40.0],
    }
    index = ["TotalRevenue", "NetIncome", "EPS"]
    return pd.DataFrame(data, index=index)


class TestIncomeStatementCommand:
    """Tests for the income-statement CLI command."""

    @patch("src.commands.financials.yf.Ticker")
    def test_income_statement_basic(self, mock_ticker):
        """Test basic income-statement command execution (yearly)."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_income_stmt.return_value = create_mock_income_statement_data(
            freq="yearly"
        )

        result = runner.invoke(app, ["income-stmt", "AAPL"])

        assert result.exit_code == 0
        assert "TotalRevenue" in result.output
        assert "1000.0" in result.output

        # Verify call args
        mock_instance.get_income_stmt.assert_called_with(pretty=True, freq="yearly")

    @patch("src.commands.financials.yf.Ticker")
    def test_income_statement_quarterly(self, mock_ticker):
        """Test income-statement command with --quarterly option."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_income_stmt.return_value = create_mock_income_statement_data(
            freq="quarterly"
        )

        result = runner.invoke(app, ["income-stmt", "AAPL", "--frequency", "quarterly"])

        assert result.exit_code == 0
        assert "2025-12-31" in result.output

        # Verify call args
        mock_instance.get_income_stmt.assert_called_with(pretty=True, freq="quarterly")

    @patch("src.commands.financials.yf.Ticker")
    def test_income_statement_no_data(self, mock_ticker):
        """Test income-statement command when no data is found."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_income_stmt.return_value = pd.DataFrame()

        result = runner.invoke(app, ["income-stmt", "AAPL"])

        assert result.exit_code == 0
        assert "[]" in result.output

    @patch("src.commands.financials.yf.Ticker")
    def test_income_statement_api_error(self, mock_ticker):
        """Test income-statement command handles API errors."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_income_stmt.side_effect = Exception("API Error")

        result = runner.invoke(app, ["income-stmt", "AAPL"])

        assert result.exit_code == 1
        assert "Unexpected error" in result.output
