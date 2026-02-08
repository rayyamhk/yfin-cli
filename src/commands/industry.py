import yfinance as yf
from ..typer import (
    IndustryKeyType,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def industry_overview(
    key: IndustryKeyType,
    output: OutputType = default_output,
):
    """
    Retrieves the overview information of the domain entity.
    """
    return yf.Industry(key).overview


@handle_errors
@with_output
def industry_research_reports(
    key: IndustryKeyType,
    output: OutputType = default_output,
):
    """
    Retrieves research reports related to the domain entity.
    """
    return yf.Industry(key).research_reports


@handle_errors
@with_output
def industry_top_companies(
    key: IndustryKeyType,
    output: OutputType = default_output,
):
    """
    Retrieves the top companies within the domain entity.
    """
    return yf.Industry(key).top_companies


@handle_errors
@with_output
def industry_top_growth_companies(
    key: IndustryKeyType,
    output: OutputType = default_output,
):
    """
    Returns the top growth companies in the industry.
    """
    return yf.Industry(key).top_growth_companies


@handle_errors
@with_output
def industry_top_performing_companies(
    key: IndustryKeyType,
    output: OutputType = default_output,
):
    """
    Returns the top performing companies in the industry.
    """
    return yf.Industry(key).top_performing_companies
