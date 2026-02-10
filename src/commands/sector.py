import yfinance as yf
from ..typer import SectorKeyType
from ..decorators import command
from ..utils import data_frame_to_list


@command
def sector_keys():
    """
    Get all available sector keys.
    """
    return [{"key": k} for k in yf.const.SECTOR_INDUSTY_MAPPING_LC.keys()]


@command
def sector_industries(key: SectorKeyType):
    """
    Get the industries within a sector.
    """
    return data_frame_to_list(yf.Sector(key).industries)


@command
def sector_overview(key: SectorKeyType):
    """
    Get the overview information of the domain entity.
    """
    return yf.Sector(key).overview


@command
def sector_research_reports(key: SectorKeyType):
    """
    Get research reports related to the domain entity.
    """
    return yf.Sector(key).research_reports


@command
def sector_top_companies(key: SectorKeyType):
    """
    Get the top companies within the domain entity.
    """
    return data_frame_to_list(yf.Sector(key).top_companies)


@command
def sector_top_etfs(key: SectorKeyType):
    """
    Get the top ETFs for the sector.
    """
    return [
        {"symbol": symbol, "name": name}
        for symbol, name in yf.Sector(key).top_etfs.items()
    ]


@command
def sector_top_mutual_funds(key: SectorKeyType):
    """
    Get the top mutual funds for the sector.
    """
    return [
        {"symbol": symbol, "name": name}
        for symbol, name in yf.Sector(key).top_mutual_funds.items()
    ]
