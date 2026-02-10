"""Tests for the news command."""

from unittest.mock import patch


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


@patch("src.commands.stock.yf.Ticker")
def test_news_basic(mock_ticker, invoke_json):
    mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES
    code, data = invoke_json("news", "TSLA")

    assert code == 0
    assert len(data) == 2
    assert data[0]["Title"] == "Test Article Title"
    assert data[0]["Source"] == "Test Source"
    assert data[0]["URL"] == "https://example.com/article"
    assert data[1]["Title"] == "Another Test Article"


@patch("src.commands.stock.yf.Ticker")
def test_news_with_count(mock_ticker, invoke):
    mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES[:1]
    result = invoke("news", "TSLA", "--count", "1")

    assert result.exit_code == 0
    mock_ticker.return_value.get_news.assert_called_once_with(1, "all")


@patch("src.commands.stock.yf.Ticker")
def test_news_with_tab(mock_ticker, invoke):
    mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES
    result = invoke("news", "TSLA", "--tab", "news")

    assert result.exit_code == 0
    mock_ticker.return_value.get_news.assert_called_once_with(5, "news")


def test_news_invalid_tab(invoke):
    result = invoke("news", "TSLA", "--tab", "invalid")
    assert result.exit_code == 2
    assert "Invalid" in result.output


@patch("src.commands.stock.yf.Ticker")
def test_news_empty_articles(mock_ticker, invoke_json):
    mock_ticker.return_value.get_news.return_value = []
    code, data = invoke_json("news", "TSLA")

    assert code == 0
    assert data == []


@patch("src.commands.stock.yf.Ticker")
def test_news_ticker_uppercase(mock_ticker, invoke):
    mock_ticker.return_value.get_news.return_value = MOCK_ARTICLES
    invoke("news", "tsla")
    mock_ticker.assert_called_once_with("TSLA")


@patch("src.commands.stock.yf.Ticker")
def test_news_api_error(mock_ticker, invoke):
    mock_ticker.return_value.get_news.side_effect = Exception("API Error")
    result = invoke("news", "TSLA")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
