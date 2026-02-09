import yfinance as yf
from ..typer import IndustryKeyType
from ..decorators import handle_errors, with_output
from ..utils import data_frame_to_list


@handle_errors
@with_output
def industry_overview(key: IndustryKeyType):
    """
    Get the overview information of the domain entity.
    """
    return yf.Industry(key).overview


@handle_errors
@with_output
def industry_research_reports(key: IndustryKeyType):
    """
    Get research reports related to the domain entity.
    """
    return yf.Industry(key).research_reports


@handle_errors
@with_output
def industry_top_companies(key: IndustryKeyType):
    """
    Get the top companies within the domain entity.
    """
    return data_frame_to_list(yf.Industry(key).top_companies)


@handle_errors
@with_output
def industry_top_growth_companies(key: IndustryKeyType):
    """
    Get the top growth companies in the industry.
    """
    return data_frame_to_list(yf.Industry(key).top_growth_companies)


@handle_errors
@with_output
def industry_top_performing_companies(key: IndustryKeyType):
    """
    Get the top performing companies in the industry.
    """
    return data_frame_to_list(yf.Industry(key).top_performing_companies)
