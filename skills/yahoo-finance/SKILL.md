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
## Reading the Output

### Success, empty results, and errors

- **Success**: exit code `0`, JSON on stdout (a list of objects, or one object).
- **Empty list `[]`**: the ticker exists but has no data of that kind (e.g. `income-stmt` for an ETF). It is not an error.
- **Error**: exit code `1`, nothing on stdout, and one JSON line on stderr:

  ```json
  {"error": "not_found", "message": "Ticker 'XYZ' not found on Yahoo Finance"}
  ```

  | `error`     | Meaning                                                                           |
  | ----------- | --------------------------------------------------------------------------------- |
  | `not_found` | The ticker doesn't exist (or is delisted). Check the symbol and its exchange suffix (e.g. `7203.T`, `VOD.L`). |
  | `no_data`   | Nothing returned; for sector/industry commands the key is likely wrong (the message says how to list valid keys). |
  | `error`     | Anything else (network, Yahoo outage, rate limit). Retrying may help.               |

- **Invalid arguments**: exit code `2` with a usage message on stderr.

### Dates

- Daily or longer data uses the **exchange's local date**, as `YYYY-MM-DD` (a Tokyo bar for Nov 6 is `2026-11-06`).
- Timestamps keep their time and **UTC offset** (e.g. `2026-11-11T09:30:00-05:00`). Timestamps without an offset are as Yahoo provides them.

### Percentages: check the units

Yahoo mixes two conventions, sometimes for the same quantity. Before reporting a percentage, check which one the field uses.

**Fractions** (`0.0663` means 6.63%): this is the default for ratios, e.g. `pctHeld`, `pctChange`, `heldPercentInsiders`, `heldPercentInstitutions`, `shortPercentOfFloat`, `payoutRatio`, `profitMargins`, `grossMargins`, `revenueGrowth`, `earningsGrowth`, `52WeekChange`, `trailingAnnualDividendYield`, `ytd return`, `market weight`, `growth`, `stockTrend`/`indexTrend`, and `surprisePercent` in `earnings-history`. Values in `major-holders` are fractions too, except `institutionsCount`.

**Already percentages** (`5.8` means 5.8%):

| Command(s)              | Fields                                                     |
| ----------------------- | ---------------------------------------------------------- |
| `earnings-dates`        | `Surprise(%)`                                              |
| `info`, `screen`        | `dividendYield`, `fiveYearAvgDividendYield`                |
| `info`, `screen`        | `regularMarketChangePercent`, `fiftyTwoWeekChangePercent`  |

For example, the same quarter's earnings surprise is `5.8` in `earnings-dates` but `0.058` in `earnings-history`.
