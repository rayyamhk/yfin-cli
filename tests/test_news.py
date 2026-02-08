"""Tests for the news command."""

from typer.testing import CliRunner
from unittest.mock import patch
from src.cli import app

runner = CliRunner()


# Mock article data for testing
MOCK_ARTICLES = [
    {
        "id": "test-1",
        "content": {
            "pubDate": "2026-02-06T17:30:54Z",
            "title": "Test Article Title",
            "summary": "Test article summary content.",
            "canonicalUrl": {"url": "https://example.com/article"},
            "provider": {"displayName": "Test Source"},
        },
    },
    {
        "id": "test-2",
        "content": {
            "pubDate": "2026-02-05T10:00:00Z",
            "title": "Another Test Article",
            "summary": "Another test summary.",
            "canonicalUrl": {"url": "https://example.com/article2"},
            "provider": {"displayName": "Another Source"},
        },
    },
]


class TestNewsCommand:
    """Tests for the news CLI command."""

    @patch("src.commands.news.yf.Ticker")
    def test_news_basic(self, mock_ticker):
        """Test basic news command execution."""
        mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES
        result = runner.invoke(app, ["news", "TSLA"])
        assert result.exit_code == 0
        # Rich table may wrap text, so check for partial match
        assert "Test Article" in result.stdout

    @patch("src.commands.news.yf.Ticker")
    def test_news_with_count(self, mock_ticker):
        """Test news command with --count option."""
        mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES[:1]
        result = runner.invoke(app, ["news", "TSLA", "--count", "1"])
        assert result.exit_code == 0
        mock_ticker.return_value.get_news.assert_called_once_with(1, "all")

    @patch("src.commands.news.yf.Ticker")
    def test_news_with_tab(self, mock_ticker):
        """Test news command with --tab option."""
        mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES
        result = runner.invoke(app, ["news", "TSLA", "--tab", "news"])
        assert result.exit_code == 0
        mock_ticker.return_value.get_news.assert_called_once_with(5, "news")

    def test_news_invalid_tab(self):
        """Test news command with invalid tab option."""
        result = runner.invoke(app, ["news", "TSLA", "--tab", "invalid"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    @patch("src.commands.news.yf.Ticker")
    def test_news_no_articles(self, mock_ticker):
        """Test news command when no articles are found."""
        mock_ticker.return_value.get_news.return_value = []
        result = runner.invoke(app, ["news", "TSLA"])
        assert result.exit_code == 1
        assert "No data found" in result.output

    @patch("src.commands.news.yf.Ticker")
    def test_news_ticker_uppercase(self, mock_ticker):
        """Test that ticker is converted to uppercase."""
        mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES
        runner.invoke(app, ["news", "tsla"])
        mock_ticker.assert_called_once_with("TSLA")

    @patch("src.commands.news.yf.Ticker")
    def test_news_api_error(self, mock_ticker):
        """Test news command handles API errors gracefully."""
        mock_ticker.return_value.get_news.side_effect = Exception("API Error")
        result = runner.invoke(app, ["news", "TSLA"])
        assert result.exit_code == 1
        assert "Unexpected error" in result.output

