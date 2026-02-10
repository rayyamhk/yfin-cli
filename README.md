# yfin-cli

A command-line interface for [Yahoo Finance](https://finance.yahoo.com/) data, powered by [yfinance](https://github.com/ranaroussi/yfinance).

## Features

### Stock Data
- **Historical Data** - OHLCV data with customizable intervals and date ranges
- **Dividends** - Dividend history for any stock
- **Fast Info** - Quick summary of key metrics (price, market cap, 52-week range)
- **News** - Latest news articles for a ticker

### Market
- **Market Status** - Current US market status (open/closed, trading hours, timezone)

### Financial Statements
- **Income Statement** - Revenue, expenses, net income
- **Balance Sheet** - Assets, liabilities, equity
- **Cash Flow** - Operating, investing, financing activities
- **Earnings Dates** - Past and upcoming earnings with EPS estimates
- **SEC Filings** - SEC filings for a ticker

### Analyst Data
- **Recommendations** - Buy/sell/hold ratings summary
- **Upgrades/Downgrades** - Analyst rating changes history
- **Price Targets** - Analyst price target estimates
- **Earnings/Revenue Estimates** - Forward-looking estimates
- **EPS Trend & Revisions** - Earnings per share analysis
- **Growth Estimates** - Projected growth rates

### Insider & Institutional
- **Insider Purchases/Transactions** - Insider trading activity
- **Major Holders** - Top shareholders
- **Institutional Holders** - Institutional ownership
- **Mutual Fund Holders** - Mutual fund ownership

### Calendar Events
- **Earnings Calendar** - Upcoming earnings releases
- **IPO Calendar** - Upcoming IPOs
- **Economic Events** - Economic indicators and releases

### Sector & Industry Analysis
- **Sector Commands** - Industries, overview, top companies, ETFs, mutual funds
- **Industry Commands** - Overview, top companies, growth companies, top performers

### Stock Screener
- **Screen** - Filter stocks by criteria (sector, market cap, beta, etc.)
- **Predefined Queries** - Use built-in screeners (day gainers, most actives, undervalued stocks)
- **JSON Queries** - Complex nested AND/OR logic for advanced screening

## Installation

### Using uv (Recommended)

```bash
uv tool install .
```

### Using pip

```bash
pip install .
```

## Usage

```bash
yfin [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output format (`json`, `table`) | `json` |
| `--help` | Show help message | — |

### Quick Examples

```bash
# Get historical stock data
yfin history AAPL

# Get quick summary metrics
yfin fast-info TSLA

# Check market status
yfin market-status

# View quarterly income statement
yfin income-stmt MSFT --frequency quarterly

# Get analyst recommendations
yfin recommendations NVDA

# Screen stocks
yfin screen --filter "sector eq Technology" --filter "intradaymarketcap gt 100000000000"

# Use a predefined screener
yfin screen --predefined day_gainers

# Output as a table
yfin --output table history AAPL --period 1y
```

> For the complete command reference with all options and parameters, see [COMMANDS.md](COMMANDS.md).

## Available Commands

| Category | Commands |
|----------|----------|
| **Stock** | `history`, `dividends`, `fast-info`, `news` |
| **Market** | `market-status` |
| **Calendar** | `calendar-earnings`, `calendar-economic-events`, `calendar-ipo` |
| **Financials** | `income-stmt`, `balance-sheet`, `cashflow`, `earnings-dates`, `sec-filings` |
| **Analysis** | `recommendations`, `upgrades-downgrades`, `price-targets`, `earnings-estimate`, `revenue-estimate`, `earnings-history`, `eps-trend`, `eps-revisions`, `growth-estimates` |
| **Holders** | `insider-purchases`, `insider-transactions`, `insider-roster-holders`, `major-holders`, `institutional-holders`, `mutualfund-holders` |
| **Sector** | `sector-keys`, `sector-industries`, `sector-overview`, `sector-research-reports`, `sector-top-companies`, `sector-top-etfs`, `sector-top-mutual-funds` |
| **Industry** | `industry-overview`, `industry-research-reports`, `industry-top-companies`, `industry-top-growth-companies`, `industry-top-performing-companies` |
| **Screen** | `screen`, `screen-query-fields`, `screen-query-values`, `screen-predefined-queries` |

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync

# Run the CLI
uv run yfin --help

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Build package
uv build
```

## License

MIT
