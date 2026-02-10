"""Tests for industry commands."""

import pandas as pd
from unittest.mock import patch


MOCK_OVERVIEW = {
    "symbol": "software-infrastructure",
    "name": "Software—Infrastructure",
    "companyCount": 120,
}

MOCK_RESEARCH_REPORTS = [
    {
        "reportTitle": "Software Outlook",
        "provider": "Argus",
        "reportDate": "2026-02-01",
    },
]

MOCK_TOP_COMPANIES = pd.DataFrame(
    {
        "name": ["Microsoft Corp", "Oracle Corp"],
        "rating_overall": ["outperform", "neutral"],
    },
    index=["MSFT", "ORCL"],
)

MOCK_GROWTH_COMPANIES = pd.DataFrame(
    {
        "name": ["CrowdStrike", "Datadog"],
        "growth": [0.32, 0.28],
    },
    index=["CRWD", "DDOG"],
)

MOCK_PERFORMING_COMPANIES = pd.DataFrame(
    {
        "name": ["ServiceNow", "Palo Alto"],
        "performance": [0.45, 0.38],
    },
    index=["NOW", "PANW"],
)


# ── industry-overview ────────────────────────────────────────────────


@patch("src.commands.industry.yf.Industry")
def test_industry_overview_basic(mock_industry, invoke_json):
    mock_industry.return_value.overview = MOCK_OVERVIEW
    code, data = invoke_json("industry-overview", "software-infrastructure")

    assert code == 0
    assert data["name"] == "Software—Infrastructure"
    assert data["companyCount"] == 120


@patch("src.commands.industry.yf.Industry")
def test_industry_overview_none_data(mock_industry, invoke):
    mock_industry.return_value.overview = None
    result = invoke("industry-overview", "software-infrastructure")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.industry.yf.Industry")
def test_industry_overview_api_error(mock_industry, invoke):
    mock_industry.side_effect = Exception("API Error")
    result = invoke("industry-overview", "software-infrastructure")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output


# ── industry-research-reports ────────────────────────────────────────


@patch("src.commands.industry.yf.Industry")
def test_industry_research_reports_basic(mock_industry, invoke_json):
    mock_industry.return_value.research_reports = MOCK_RESEARCH_REPORTS
    code, data = invoke_json("industry-research-reports", "software-infrastructure")

    assert code == 0
    assert len(data) == 1
    assert data[0]["reportTitle"] == "Software Outlook"


@patch("src.commands.industry.yf.Industry")
def test_industry_research_reports_none_data(mock_industry, invoke):
    mock_industry.return_value.research_reports = None
    result = invoke("industry-research-reports", "software-infrastructure")

    assert result.exit_code == 1
    assert "No data found" in result.output


# ── industry-top-companies ───────────────────────────────────────────


@patch("src.commands.industry.yf.Industry")
def test_industry_top_companies_basic(mock_industry, invoke_json):
    mock_industry.return_value.top_companies = MOCK_TOP_COMPANIES
    code, data = invoke_json("industry-top-companies", "software-infrastructure")

    assert code == 0
    assert len(data) == 2


@patch("src.commands.industry.yf.Industry")
def test_industry_top_companies_none_data(mock_industry, invoke):
    mock_industry.return_value.top_companies = None
    result = invoke("industry-top-companies", "software-infrastructure")

    assert result.exit_code == 1
    assert "No data found" in result.output


# ── industry-top-growth-companies ────────────────────────────────────


@patch("src.commands.industry.yf.Industry")
def test_industry_top_growth_companies_basic(mock_industry, invoke_json):
    mock_industry.return_value.top_growth_companies = MOCK_GROWTH_COMPANIES
    code, data = invoke_json("industry-top-growth-companies", "software-infrastructure")

    assert code == 0
    assert len(data) == 2


@patch("src.commands.industry.yf.Industry")
def test_industry_top_growth_companies_none_data(mock_industry, invoke):
    mock_industry.return_value.top_growth_companies = None
    result = invoke("industry-top-growth-companies", "software-infrastructure")

    assert result.exit_code == 1
    assert "No data found" in result.output


# ── industry-top-performing-companies ────────────────────────────────


@patch("src.commands.industry.yf.Industry")
def test_industry_top_performing_companies_basic(mock_industry, invoke_json):
    mock_industry.return_value.top_performing_companies = MOCK_PERFORMING_COMPANIES
    code, data = invoke_json(
        "industry-top-performing-companies", "software-infrastructure"
    )

    assert code == 0
    assert len(data) == 2


@patch("src.commands.industry.yf.Industry")
def test_industry_top_performing_companies_none_data(mock_industry, invoke):
    mock_industry.return_value.top_performing_companies = None
    result = invoke("industry-top-performing-companies", "software-infrastructure")

    assert result.exit_code == 1
    assert "No data found" in result.output


@patch("src.commands.industry.yf.Industry")
def test_industry_top_performing_companies_api_error(mock_industry, invoke):
    mock_industry.side_effect = Exception("API Error")
    result = invoke("industry-top-performing-companies", "software-infrastructure")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
