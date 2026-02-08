import yfinance as yf
from ..typer import (
    TickerType,
    OutputType,
    default_output,
)
from ..decorators import handle_errors, with_output


@handle_errors
@with_output
def recommendations(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst recommendations for a stock ticker: number of buy, sell and hold in different time periods.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_recommendations()
    return data_frame


@handle_errors
@with_output
def upgrades_downgrades(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get the analyst upgrades and downgrades history for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_upgrades_downgrades()
    return data_frame


@handle_errors
@with_output
def price_targets(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get the analyst price targets for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_analyst_price_targets()
    return data_frame


@handle_errors
@with_output
def earnings_estimate(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst earnings estimate for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_earnings_estimate()
    return data_frame


@handle_errors
@with_output
def revenue_estimate(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst revenue estimate for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_revenue_estimate()
    return data_frame


@handle_errors
@with_output
def earnings_history(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst earnings history for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_earnings_history()
    return data_frame


@handle_errors
@with_output
def eps_trend(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst eps trend for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_eps_trend()
    return data_frame


@handle_errors
@with_output
def eps_revisions(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst eps revisions for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_eps_revisions()
    return data_frame


@handle_errors
@with_output
def growth_estimates(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get analyst growth estimates for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_growth_estimates()
    return data_frame


@handle_errors
@with_output
def insider_purchases(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get insider purchases for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_insider_purchases()
    return data_frame


@handle_errors
@with_output
def insider_transactions(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get insider transactions for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_insider_transactions()
    return data_frame


@handle_errors
@with_output
def insider_roster_holders(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get insider roster holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_insider_roster_holders()
    return data_frame


@handle_errors
@with_output
def major_holders(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get major holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_major_holders()
    return data_frame


@handle_errors
@with_output
def institutional_holders(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get institutional holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_institutional_holders()
    return data_frame


@handle_errors
@with_output
def mutualfund_holders(
    ticker: TickerType,
    output: OutputType = default_output,
):
    """
    Get mutual fund holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_mutualfund_holders()
    return data_frame
