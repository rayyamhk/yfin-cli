---
name: yahoo-finance
description: Provides comprehensive financial market data and news from Yahoo Finance. Use this when the user needs to screen for stocks using granular filters, or requires historical price data, news articles, financial statements, and sector analysis.
---

# Yahoo Finance

`yfin` is the ultimate command-line interface for financial data, it provides immediate access to a massive spectrum of market intelligence—from historical price data and real-time news to deep-dive corporate financials, earnings calendars, and institutional holding records. While it excels at standard lookups across sectors and industries, the tool's true power lies in its robust stock screener: a highly flexible query engine capable of handling complex boolean logic and granular filtering, empowering you to search for and isolate exactly the assets you need based on virtually any criteria.

## Prerequisites

Assume `yfin` is already installed. However, if you attempt to run a `yfin` command and receive a "command not found" error, you MUST install it using one of the following methods:

```bash
uv tool install yfin-cli
# or
pipx install yfin-cli
# or
pip install yfin-cli
```

## Quick Examples

```bash
# Get historical stock data
yfin history AAPL

# Get quick summary metrics
yfin fast-info TSLA

# Get news for a stock
yfin news MSFT

# Check market status
yfin market-status

# View quarterly income statement
yfin income-stmt MSFT --frequency quarterly

# Screen stocks by simple filters
yfin screen --filter "sector eq Technology" --filter "intradaymarketcap gt 100000000000"

# Use a predefined screener
yfin screen --predefined day_gainers

# Screen stocks by complex filters
yfin screen --json-query '{ "operator": "and", "queries": ["region eq us", "intradaymarketcap gte 2000000000", "dayvolume gt 5000000"] }' --sort-field dayvolume --sort-order desc --limit 5

```

## Available Commands

For the complete command reference with all options and parameters, see the corresponding reference.

| Category       | Commands                                                                                                                                                                                                                                                                                                        | Reference                  |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Stock**      | `history`, `dividends`, `fast-info`, `info`, `news`, `market-status`                                                                                                                                                                                                                                            | `references/stock.md`      |
| **Calendar**   | `calendar-earnings`, `calendar-economic-events`, `calendar-ipo`                                                                                                                                                                                                                                                 | `references/calendar.md`   |
| **Financials** | `income-stmt`, `balance-sheet`, `cashflow`, `earnings-dates`, `sec-filings`                                                                                                                                                                                                                                     | `references/financials.md` |
| **Analysis**   | `recommendations`, `upgrades-downgrades`, `price-targets`, `earnings-estimate`, `revenue-estimate`, `earnings-history`, `eps-trend`, `eps-revisions`, `growth-estimates`, `insider-purchases`, `insider-transactions`, `insider-roster-holders`, `major-holders`, `institutional-holders`, `mutualfund-holders` | `references/analysis.md`   |
| **Screen**     | `screen`, `screen-query-fields`, `screen-query-values`, `screen-predefined-queries`                                                                                                                                                                                                                             | `references/screen.md`     |
| **Sector**     | `sector-keys`, `sector-industries`, `sector-overview`, `sector-research-reports`, `sector-top-companies`, `sector-top-etfs`, `sector-top-mutual-funds`                                                                                                                                                          | `references/sector.md`     |
| **Industry**   | `industry-overview`, `industry-research-reports`, `industry-top-companies`, `industry-top-growth-companies`, `industry-top-performing-companies`                                                                                                                                                                | `references/industry.md`   |