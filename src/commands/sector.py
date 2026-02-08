import pandas as pd
import yfinance as yf
from ..typer import SectorKeyType
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def sector_keys():
    """
    Get all available sector keys.
    """
    data = [
        ["basic-materials", "Basic Materials"],
        ["communication-services", "Communication Services"],
        ["consumer-cyclical", "Consumer Cyclical"],
        ["consumer-defensive", "Consumer Defensive"],
        ["energy", "Energy"],
        ["financial-services", "Financial Services"],
        ["healthcare", "Healthcare"],
        ["industrials", "Industrials"],
        ["real-estate", "Real Estate"],
        ["technology", "Technology"],
        ["utilities", "Utilities"],
    ]
    return pd.DataFrame(data, columns=["key", "name"])


@handle_errors
@with_output
def sector_industries(key: SectorKeyType):
    """
    Get the industries within a sector.
    """
    return yf.Sector(key).industries


@handle_errors
@with_output
def sector_overview(key: SectorKeyType):
    """
    Get the overview information of the domain entity.
    """
    return yf.Sector(key).overview


@handle_errors
@with_output
def sector_research_reports(key: SectorKeyType):
    """
    Get research reports related to the domain entity.
    """
    return yf.Sector(key).research_reports


@handle_errors
@with_output
def sector_top_companies(key: SectorKeyType):
    """
    Get the top companies within the domain entity.
    """
    return yf.Sector(key).top_companies


@handle_errors
@with_output
def sector_top_etfs(key: SectorKeyType):
    """
    Get the top ETFs for the sector.
    """
    return yf.Sector(key).top_etfs


@handle_errors
@with_output
def sector_top_mutual_funds(key: SectorKeyType):
    """
    Get the top mutual funds for the sector.
    """
    return yf.Sector(key).top_mutual_funds
