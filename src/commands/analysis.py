import yfinance as yf
from ..typer import TickerType
from ..decorators import command
from ..utils import data_frame_to_list


@command
def recommendations(ticker: TickerType):
    """
    Get analyst recommendations for a stock ticker: number of buy, sell and hold in different time periods.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_recommendations()
    return data_frame_to_list(data_frame)


@command
def upgrades_downgrades(ticker: TickerType):
    """
    Get the analyst upgrades and downgrades history for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_upgrades_downgrades()
    return data_frame_to_list(data_frame)


@command
def price_targets(ticker: TickerType):
    """
    Get the analyst price targets for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    return stock.get_analyst_price_targets()


@command
def earnings_estimate(ticker: TickerType):
    """
    Get analyst earnings estimate for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_earnings_estimate()
    return data_frame_to_list(data_frame)


@command
def revenue_estimate(ticker: TickerType):
    """
    Get analyst revenue estimate for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_revenue_estimate()
    return data_frame_to_list(data_frame)


@command
def earnings_history(ticker: TickerType):
    """
    Get analyst earnings history for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_earnings_history()
    return data_frame_to_list(data_frame)


@command
def eps_trend(ticker: TickerType):
    """
    Get analyst eps trend for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_eps_trend()
    return data_frame_to_list(data_frame)


@command
def eps_revisions(ticker: TickerType):
    """
    Get analyst eps revisions for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_eps_revisions()
    return data_frame_to_list(data_frame)


@command
def growth_estimates(ticker: TickerType):
    """
    Get analyst growth estimates for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_growth_estimates()
    return data_frame_to_list(data_frame)


@command
def insider_purchases(ticker: TickerType):
    """
    Get insider purchases for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_insider_purchases()
    return data_frame_to_list(data_frame)


@command
def insider_transactions(ticker: TickerType):
    """
    Get insider transactions for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_insider_transactions()
    return data_frame_to_list(data_frame)


@command
def insider_roster_holders(ticker: TickerType):
    """
    Get insider roster holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_insider_roster_holders()
    return data_frame_to_list(data_frame)


@command
def major_holders(ticker: TickerType):
    """
    Get major holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_major_holders()
    return data_frame_to_list(data_frame, index_name="Breakdown")


@command
def institutional_holders(ticker: TickerType):
    """
    Get institutional holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_institutional_holders()
    return data_frame_to_list(data_frame)


@command
def mutualfund_holders(ticker: TickerType):
    """
    Get mutual fund holders for a stock ticker.
    """
    stock = yf.Ticker(ticker)
    data_frame = stock.get_mutualfund_holders()
    return data_frame_to_list(data_frame)
