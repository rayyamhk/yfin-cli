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
| `--output` | Output format (`table`) | `table` |
| `--help` | Show help message | - |

### Examples

**Get historical data:**
```bash
yfin history AAPL --period 1mo --interval 1d
```

**View income statement (quarterly):**
```bash
yfin income-stmt MSFT --frequency quarterly
```

**Get analyst recommendations:**
```bash
yfin recommendations NVDA
```

**Check insider transactions:**
```bash
yfin insider-transactions TSLA
```

**View sector top companies (table format):**
```bash
yfin --output table sector-top-companies technology
```

**Get industry top performers:**
```bash
yfin industry-top-performing-companies aluminum
```

**Screen stocks by sector and market cap:**
```bash
yfin screen --filter "sector eq Technology" --filter "intradaymarketcap gt 100000000000"
```

**Use a predefined screener:**
```bash
yfin screen --predefined day_gainers
```

**View earnings calendar:**
```bash
yfin calendar-earnings --start 2026-02-01 --end 2026-02-28
```

**Get recent news:**
```bash
yfin news GOOGL --count 10
```

## Available Commands

| Category | Commands |
|----------|----------|
| **Stock** | `history`, `dividends`, `fast-info`, `news` |
| **Market** | `market-status` |
| **Financials** | `income-stmt`, `balance-sheet`, `cashflow`, `earnings-dates`, `sec-filings` |
| **Analysis** | `recommendations`, `upgrades-downgrades`, `price-targets`, `earnings-estimate`, `revenue-estimate`, `earnings-history`, `eps-trend`, `eps-revisions`, `growth-estimates` |
| **Holders** | `insider-purchases`, `insider-transactions`, `insider-roster-holders`, `major-holders`, `institutional-holders`, `mutualfund-holders` |
| **Calendar** | `calendar-earnings`, `calendar-ipo`, `calendar-economic-events` |
| **Sector** | `sector-industries`, `sector-overview`, `sector-research-reports`, `sector-top-companies`, `sector-top-etfs`, `sector-top-mutual-funds` |
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
