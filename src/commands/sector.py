import yfinance as yf
from ..typer import SectorKeyType
from ..decorators import handle_errors, with_output


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
    Retrieves the overview information of the domain entity.
    """
    return yf.Sector(key).overview


@handle_errors
@with_output
def sector_research_reports(key: SectorKeyType):
    """
    Retrieves research reports related to the domain entity.
    """
    return yf.Sector(key).research_reports


@handle_errors
@with_output
def sector_top_companies(key: SectorKeyType):
    """
    Retrieves the top companies within the domain entity.
    """
    return yf.Sector(key).top_companies


@handle_errors
@with_output
def sector_top_etfs(key: SectorKeyType):
    """
    Gets the top ETFs for the sector.
    """
    return yf.Sector(key).top_etfs


@handle_errors
@with_output
def sector_top_mutual_funds(key: SectorKeyType):
    """
    Gets the top mutual funds for the sector.
    """
    return yf.Sector(key).top_mutual_funds
