"""Tests for the balance-sheet command."""

import pandas as pd
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from src.cli import app

runner = CliRunner()


# Mock Balance Sheet data for testing
def create_mock_balance_sheet_data(freq="yearly"):
    """Create a mock pandas DataFrame similar to yf.Ticker.get_balance_sheet output."""
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

    data = {
        dates[0]: [10000.0, 5000.0],
        dates[1]: [9000.0, 4500.0],
        dates[2]: [8000.0, 4000.0],
    }
    index = ["TotalAssets", "TotalLiabilities"]
    return pd.DataFrame(data, index=index)


class TestBalanceSheetCommand:
    """Tests for the balance-sheet CLI command."""

    @patch("src.commands.balance_sheet.yf.Ticker")
    def test_balance_sheet_basic(self, mock_ticker):
        """Test basic balance-sheet command execution (yearly)."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_balance_sheet.return_value = create_mock_balance_sheet_data(
            freq="yearly"
        )

        result = runner.invoke(app, ["balance-sheet", "MSFT"])

        assert result.exit_code == 0
        assert "TotalAssets" in result.output
        assert "10000.0" in result.output

        # Verify call args
        mock_instance.get_balance_sheet.assert_called_with(pretty=True, freq="yearly")

    @patch("src.commands.balance_sheet.yf.Ticker")
    def test_balance_sheet_quarterly(self, mock_ticker):
        """Test balance-sheet command with --frequency quarterly."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_balance_sheet.return_value = create_mock_balance_sheet_data(
            freq="quarterly"
        )

        result = runner.invoke(
            app, ["balance-sheet", "MSFT", "--frequency", "quarterly"]
        )

        assert result.exit_code == 0
        # 2025-03-31 should be in columns
        assert "2025-03-31" in result.output

        # Verify call args
        mock_instance.get_balance_sheet.assert_called_with(
            pretty=True, freq="quarterly"
        )

    @patch("src.commands.balance_sheet.yf.Ticker")
    def test_balance_sheet_no_data(self, mock_ticker):
        """Test balance-sheet command when no data is found."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_balance_sheet.return_value = pd.DataFrame()

        result = runner.invoke(app, ["balance-sheet", "MSFT"])

        # Typer exit code 1 raised explicitly
        assert result.exit_code == 1
        assert "No data found" in result.output

    @patch("src.commands.balance_sheet.yf.Ticker")
    def test_balance_sheet_api_error(self, mock_ticker):
        """Test balance-sheet command handles API errors."""
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        mock_instance.get_balance_sheet.side_effect = Exception("API Error")

        result = runner.invoke(app, ["balance-sheet", "MSFT"])

        assert result.exit_code == 1
        assert "Unexpected error" in result.output
