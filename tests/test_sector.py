"""Tests for sector commands."""

import pandas as pd
from unittest.mock import patch


MOCK_INDUSTRIES = pd.DataFrame(
    {"name": ["Software", "Semiconductors"], "key": ["software", "semiconductors"]},
)

MOCK_OVERVIEW = {
    "symbol": "technology",
    "name": "Technology",
    "companyCount": 1500,
}

MOCK_RESEARCH_REPORTS = [
    {
        "reportTitle": "Tech Outlook 2026",
        "provider": "Argus",
        "reportDate": "2026-02-01",
    },
    {
        "reportTitle": "Sector Review",
        "provider": "Morningstar",
        "reportDate": "2026-01-15",
    },
]

MOCK_TOP_COMPANIES = pd.DataFrame(
    {
        "name": ["Apple Inc", "Microsoft Corp"],
        "rating_overall": ["outperform", "outperform"],
    },
    index=["AAPL", "MSFT"],
)

MOCK_TOP_ETFS = {
    "XLK": "Technology Select Sector SPDR",
    "VGT": "Vanguard Information Technology",
}
MOCK_TOP_MUTUAL_FUNDS = {"FTEC": "Fidelity MSCI IT", "VITAX": "Vanguard IT Admiral"}


# ── sector-keys ──────────────────────────────────────────────────────


@patch("src.commands.sector.yf.const")
def test_sector_keys(mock_const, invoke_json):
    mock_const.SECTOR_INDUSTY_MAPPING_LC = {"technology": [], "healthcare": []}
    code, data = invoke_json("sector-keys")

    assert code == 0
    assert len(data) == 2
    keys = [d["key"] for d in data]
    assert "technology" in keys
    assert "healthcare" in keys


# ── sector-industries ────────────────────────────────────────────────


@patch("src.commands.sector.yf.Sector")
def test_sector_industries_basic(mock_sector, invoke_json):
    mock_sector.return_value.industries = MOCK_INDUSTRIES
    code, data = invoke_json("sector-industries", "technology")

    assert code == 0
    assert len(data) == 2
    assert data[0]["name"] == "Software"


@patch("src.commands.sector.yf.Sector")
def test_sector_industries_api_error(mock_sector, invoke):
    mock_sector.side_effect = Exception("API Error")
    result = invoke("sector-industries", "technology")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output


# ── sector-overview ──────────────────────────────────────────────────


@patch("src.commands.sector.yf.Sector")
def test_sector_overview_basic(mock_sector, invoke_json):
    mock_sector.return_value.overview = MOCK_OVERVIEW
    code, data = invoke_json("sector-overview", "technology")

    assert code == 0
    assert data["name"] == "Technology"
    assert data["companyCount"] == 1500


@patch("src.commands.sector.yf.Sector")
def test_sector_overview_none_data(mock_sector, invoke):
    mock_sector.return_value.overview = None
    result = invoke("sector-overview", "technology")

    assert result.exit_code == 1
    assert "No data found" in result.output


# ── sector-research-reports ──────────────────────────────────────────


@patch("src.commands.sector.yf.Sector")
def test_sector_research_reports_basic(mock_sector, invoke_json):
    mock_sector.return_value.research_reports = MOCK_RESEARCH_REPORTS
    code, data = invoke_json("sector-research-reports", "technology")

    assert code == 0
    assert len(data) == 2
    assert data[0]["reportTitle"] == "Tech Outlook 2026"


@patch("src.commands.sector.yf.Sector")
def test_sector_research_reports_none_data(mock_sector, invoke):
    mock_sector.return_value.research_reports = None
    result = invoke("sector-research-reports", "technology")

    assert result.exit_code == 1
    assert "No data found" in result.output


# ── sector-top-companies ─────────────────────────────────────────────


@patch("src.commands.sector.yf.Sector")
def test_sector_top_companies_basic(mock_sector, invoke_json):
    mock_sector.return_value.top_companies = MOCK_TOP_COMPANIES
    code, data = invoke_json("sector-top-companies", "technology")

    assert code == 0
    assert len(data) == 2


@patch("src.commands.sector.yf.Sector")
def test_sector_top_companies_none_data(mock_sector, invoke):
    mock_sector.return_value.top_companies = None
    result = invoke("sector-top-companies", "technology")

    assert result.exit_code == 1
    assert "No data found" in result.output


# ── sector-top-etfs ──────────────────────────────────────────────────


@patch("src.commands.sector.yf.Sector")
def test_sector_top_etfs_basic(mock_sector, invoke_json):
    mock_sector.return_value.top_etfs = MOCK_TOP_ETFS
    code, data = invoke_json("sector-top-etfs", "technology")

    assert code == 0
    assert len(data) == 2
    assert data[0]["symbol"] == "XLK"
    assert data[0]["name"] == "Technology Select Sector SPDR"


@patch("src.commands.sector.yf.Sector")
def test_sector_top_etfs_api_error(mock_sector, invoke):
    mock_sector.side_effect = Exception("API Error")
    result = invoke("sector-top-etfs", "technology")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output


# ── sector-top-mutual-funds ──────────────────────────────────────────


@patch("src.commands.sector.yf.Sector")
def test_sector_top_mutual_funds_basic(mock_sector, invoke_json):
    mock_sector.return_value.top_mutual_funds = MOCK_TOP_MUTUAL_FUNDS
    code, data = invoke_json("sector-top-mutual-funds", "technology")

    assert code == 0
    assert len(data) == 2
    assert data[0]["symbol"] == "FTEC"


@patch("src.commands.sector.yf.Sector")
def test_sector_top_mutual_funds_api_error(mock_sector, invoke):
    mock_sector.side_effect = Exception("API Error")
    result = invoke("sector-top-mutual-funds", "technology")

    assert result.exit_code == 1
    assert "Unexpected error" in result.output
