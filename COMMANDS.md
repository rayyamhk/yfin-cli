# yfin CLI — Command Reference

A comprehensive reference for every command in the `yfin` CLI.

> [!TIP]
> **Global option:** All commands support `--output json` (default) and `--output table`. Use `--help` on any command for quick reference.

---

## Table of Contents

- [Stock](#stock)
  - [`history`](#history)
  - [`dividends`](#dividends)
  - [`fast-info`](#fast-info)
  - [`news`](#news)
- [Market](#market)
  - [`market-status`](#market-status)
- [Calendar](#calendar)
  - [`calendar-earnings`](#calendar-earnings)
  - [`calendar-economic-events`](#calendar-economic-events)
  - [`calendar-ipo`](#calendar-ipo)
- [Financials](#financials)
  - [`income-stmt`](#income-stmt)
  - [`balance-sheet`](#balance-sheet)
  - [`cashflow`](#cashflow)
  - [`earnings-dates`](#earnings-dates)
  - [`sec-filings`](#sec-filings)
- [Analysis](#analysis)
  - [`recommendations`](#recommendations)
  - [`upgrades-downgrades`](#upgrades-downgrades)
  - [`price-targets`](#price-targets)
  - [`earnings-estimate`](#earnings-estimate)
  - [`revenue-estimate`](#revenue-estimate)
  - [`earnings-history`](#earnings-history)
  - [`eps-trend`](#eps-trend)
  - [`eps-revisions`](#eps-revisions)
  - [`growth-estimates`](#growth-estimates)
  - [`insider-purchases`](#insider-purchases)
  - [`insider-transactions`](#insider-transactions)
  - [`insider-roster-holders`](#insider-roster-holders)
  - [`major-holders`](#major-holders)
  - [`institutional-holders`](#institutional-holders)
  - [`mutualfund-holders`](#mutualfund-holders)
- [Sector](#sector)
  - [`sector-keys`](#sector-keys)
  - [`sector-industries`](#sector-industries)
  - [`sector-overview`](#sector-overview)
  - [`sector-research-reports`](#sector-research-reports)
  - [`sector-top-companies`](#sector-top-companies)
  - [`sector-top-etfs`](#sector-top-etfs)
  - [`sector-top-mutual-funds`](#sector-top-mutual-funds)
- [Industry](#industry)
  - [`industry-overview`](#industry-overview)
  - [`industry-research-reports`](#industry-research-reports)
  - [`industry-top-companies`](#industry-top-companies)
  - [`industry-top-growth-companies`](#industry-top-growth-companies)
  - [`industry-top-performing-companies`](#industry-top-performing-companies)
- [Screen](#screen)
  - [`screen`](#screen-1)
  - [`screen-query-fields`](#screen-query-fields)
  - [`screen-query-values`](#screen-query-values)
  - [`screen-predefined-queries`](#screen-predefined-queries)

---

## Stock

### `history`

Get historical market data (OHLCV) for a stock ticker.

| Parameter    | Type     | Required | Default | Description                                                                                        |
| ------------ | -------- | -------- | ------- | -------------------------------------------------------------------------------------------------- |
| `TICKER`     | argument | ✅       | —       | Stock ticker symbol (e.g., TSLA, AAPL)                                                             |
| `--interval` | option   | —        | `1d`    | Data interval: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo` |
| `--period`   | option   | —        | `1mo`\* | Data period: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`                |
| `--start`    | option   | —        | —       | Start date (`YYYY-MM-DD`)                                                                          |
| `--end`      | option   | —        | —       | End date (`YYYY-MM-DD`)                                                                            |

> \*Default period is `1mo` when no period, start, or end is specified. At most 2 of `--period`, `--start`, `--end` can be specified together.

**Examples:**

```bash
# Get last month of daily data for Apple
yfin history AAPL

# Get 1-year weekly history
yfin history TSLA --period 1y --interval 1wk

# Get data between specific dates with 5-minute intervals
yfin history MSFT --start 2025-01-01 --end 2025-01-31 --interval 5m

# Get year-to-date history
yfin history GOOG --period ytd
```

---

### `dividends`

Get dividend history for a stock ticker.

| Parameter  | Type     | Required | Default | Description                                                                         |
| ---------- | -------- | -------- | ------- | ----------------------------------------------------------------------------------- |
| `TICKER`   | argument | ✅       | —       | Stock ticker symbol                                                                 |
| `--period` | option   | —        | `max`   | Data period: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max` |

**Examples:**

```bash
# Get all-time dividend history
yfin dividends AAPL

# Get dividends from the last 5 years
yfin dividends KO --period 5y
```

---

### `fast-info`

Get fast info (15 min delayed) summary for a stock ticker. Returns key metrics like price, market cap, volume, and 52-week range.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
# Get quick summary metrics for Tesla
yfin fast-info TSLA

# Get fast info for Microsoft
yfin fast-info MSFT
```

---

### `news`

Get news articles for a stock ticker.

| Parameter | Type     | Required | Default | Description                                      |
| --------- | -------- | -------- | ------- | ------------------------------------------------ |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol                              |
| `--count` | option   | —        | `10`    | Number of results to show                        |
| `--tab`   | option   | —        | `all`   | News tab filter: `all`, `news`, `press releases` |

**Examples:**

```bash
# Get latest 5 news articles for Apple
yfin news AAPL

# Get 10 press releases for Tesla
yfin news TSLA --count 10 --tab "press releases"

# Get 3 news articles
yfin news GOOG --count 3 --tab news
```

---

## Market

### `market-status`

Get the current US market status (open/closed, trading hours, timezone).

| Parameter | Type | Required | Default | Description            |
| --------- | ---- | -------- | ------- | ---------------------- |
| _(none)_  | —    | —        | —       | No parameters required |

**Examples:**

```bash
# Check if the US market is open
yfin market-status
```

---

## Calendar

### `calendar-earnings`

Get the earnings calendar — upcoming and recent earnings announcements.

| Parameter      | Type   | Required | Default        | Description               |
| -------------- | ------ | -------- | -------------- | ------------------------- |
| `--start`      | option | —        | today          | Start date (`YYYY-MM-DD`) |
| `--end`        | option | —        | today + 7 days | End date (`YYYY-MM-DD`)   |
| `--limit`      | option | —        | `12`           | Maximum number of results |
| `--offset`     | option | —        | `0`            | Offset for pagination     |
| `--market-cap` | option | —        | `0`            | Minimum market cap filter |

**Examples:**

```bash
# Get this week's earnings
yfin calendar-earnings

# Get earnings for a specific date range
yfin calendar-earnings --start 2026-02-10 --end 2026-02-14

# Get top 5 earnings by market cap
yfin calendar-earnings --limit 5

# Paginate results
yfin calendar-earnings --limit 10 --offset 10
```

---

### `calendar-ipo`

Get the IPO calendar — upcoming initial public offerings.

| Parameter  | Type   | Required | Default        | Description               |
| ---------- | ------ | -------- | -------------- | ------------------------- |
| `--start`  | option | —        | today          | Start date (`YYYY-MM-DD`) |
| `--end`    | option | —        | today + 7 days | End date (`YYYY-MM-DD`)   |
| `--limit`  | option | —        | `12`           | Maximum number of results |
| `--offset` | option | —        | `0`            | Offset for pagination     |

**Examples:**

```bash
# Get upcoming IPOs this week
yfin calendar-ipo

# Get IPOs for next month
yfin calendar-ipo --start 2026-03-01 --end 2026-03-31
```

---

### `calendar-economic-events`

Get the economic events calendar — scheduled economic data releases and events.

| Parameter  | Type   | Required | Default        | Description               |
| ---------- | ------ | -------- | -------------- | ------------------------- |
| `--start`  | option | —        | today          | Start date (`YYYY-MM-DD`) |
| `--end`    | option | —        | today + 7 days | End date (`YYYY-MM-DD`)   |
| `--limit`  | option | —        | `12`           | Maximum number of results |
| `--offset` | option | —        | `0`            | Offset for pagination     |

**Examples:**

```bash
# Get this week's economic events
yfin calendar-economic-events

# Get events for a specific week with more results
yfin calendar-economic-events --start 2026-02-10 --end 2026-02-14 --limit 50
```

---

## Financials

### `income-stmt`

Get the income statement for a ticker.

| Parameter     | Type     | Required | Default  | Description                                  |
| ------------- | -------- | -------- | -------- | -------------------------------------------- |
| `TICKER`      | argument | ✅       | —        | Stock ticker symbol                          |
| `--frequency` | option   | —        | `yearly` | Frequency: `yearly`, `quarterly`, `trailing` |

**Examples:**

```bash
# Get annual income statement
yfin income-stmt AAPL

# Get quarterly income statement
yfin income-stmt MSFT --frequency quarterly

# Get trailing twelve months
yfin income-stmt GOOG --frequency trailing
```

---

### `balance-sheet`

Get the balance sheet for a ticker.

| Parameter     | Type     | Required | Default  | Description                      |
| ------------- | -------- | -------- | -------- | -------------------------------- |
| `TICKER`      | argument | ✅       | —        | Stock ticker symbol              |
| `--frequency` | option   | —        | `yearly` | Frequency: `yearly`, `quarterly` |

**Examples:**

```bash
# Get annual balance sheet
yfin balance-sheet AAPL

# Get quarterly balance sheet
yfin balance-sheet TSLA --frequency quarterly
```

---

### `cashflow`

Get the cash flow statement for a ticker.

| Parameter     | Type     | Required | Default  | Description                                  |
| ------------- | -------- | -------- | -------- | -------------------------------------------- |
| `TICKER`      | argument | ✅       | —        | Stock ticker symbol                          |
| `--frequency` | option   | —        | `yearly` | Frequency: `yearly`, `quarterly`, `trailing` |

**Examples:**

```bash
# Get annual cash flow
yfin cashflow AAPL

# Get quarterly cash flow
yfin cashflow NVDA --frequency quarterly
```

---

### `earnings-dates`

Get earnings dates, estimates, and reported EPS for a ticker.

| Parameter  | Type     | Required | Default | Description               |
| ---------- | -------- | -------- | ------- | ------------------------- |
| `TICKER`   | argument | ✅       | —       | Stock ticker symbol       |
| `--limit`  | option   | —        | `12`    | Maximum number of results |
| `--offset` | option   | —        | `0`     | Offset for pagination     |

**Examples:**

```bash
# Get upcoming/recent earnings dates
yfin earnings-dates AAPL

# Get more earnings dates
yfin earnings-dates MSFT --limit 20

# Paginate to older earnings
yfin earnings-dates GOOG --limit 10 --offset 10
```

---

### `sec-filings`

Get SEC filings for a ticker.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
# Get SEC filings for Apple
yfin sec-filings AAPL
```

---

## Analysis

### `recommendations`

Get analyst recommendations — number of buy, sell, and hold ratings across time periods.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin recommendations AAPL
yfin recommendations TSLA
```

---

### `upgrades-downgrades`

Get the history of analyst upgrades and downgrades.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin upgrades-downgrades AAPL
```

---

### `price-targets`

Get analyst price targets (current, low, high, mean, median).

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin price-targets TSLA
```

---

### `earnings-estimate`

Get analyst earnings estimates for upcoming periods.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin earnings-estimate AAPL
```

---

### `revenue-estimate`

Get analyst revenue estimates for upcoming periods.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin revenue-estimate MSFT
```

---

### `earnings-history`

Get historical earnings — actual vs. estimated EPS.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin earnings-history GOOG
```

---

### `eps-trend`

Get the EPS trend — how estimates have changed over time.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin eps-trend AAPL
```

---

### `eps-revisions`

Get EPS revisions — analyst estimate changes (up/down revisions).

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin eps-revisions NVDA
```

---

### `growth-estimates`

Get analyst growth estimates for a stock.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin growth-estimates AMZN
```

---

### `insider-purchases`

Get insider purchase activity summary.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin insider-purchases AAPL
```

---

### `insider-transactions`

Get detailed insider transaction records (buys, sells, exercises).

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin insider-transactions TSLA
```

---

### `insider-roster-holders`

Get the insider roster — list of insiders and their holdings.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin insider-roster-holders MSFT
```

---

### `major-holders`

Get major holders breakdown (% held by insiders, institutions, etc.).

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin major-holders AAPL
```

---

### `institutional-holders`

Get the top institutional holders and their positions.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin institutional-holders GOOG
```

---

### `mutualfund-holders`

Get the top mutual fund holders and their positions.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
yfin mutualfund-holders MSFT
```

---

## Sector

### `sector-keys`

Get all available sector keys. Use these keys as arguments for other sector commands.

| Parameter | Type | Required | Default | Description            |
| --------- | ---- | -------- | ------- | ---------------------- |
| _(none)_  | —    | —        | —       | No parameters required |

**Examples:**

```bash
# List all sector keys
yfin sector-keys
```

---

### `sector-industries`

Get the industries within a sector.

| Parameter | Type     | Required | Default | Description                                         |
| --------- | -------- | -------- | ------- | --------------------------------------------------- |
| `KEY`     | argument | ✅       | —       | A valid sector key (use `yfin sector-keys` to find) |

**Examples:**

```bash
# Get industries in Technology sector
yfin sector-industries technology

# Get industries in Healthcare sector
yfin sector-industries healthcare
```

---

### `sector-overview`

Get overview information for a sector.

| Parameter | Type     | Required | Default | Description        |
| --------- | -------- | -------- | ------- | ------------------ |
| `KEY`     | argument | ✅       | —       | A valid sector key |

**Examples:**

```bash
yfin sector-overview technology
yfin sector-overview energy
```

---

### `sector-research-reports`

Get research reports related to a sector.

| Parameter | Type     | Required | Default | Description        |
| --------- | -------- | -------- | ------- | ------------------ |
| `KEY`     | argument | ✅       | —       | A valid sector key |

**Examples:**

```bash
yfin sector-research-reports financial-services
```

---

### `sector-top-companies`

Get the top companies within a sector.

| Parameter | Type     | Required | Default | Description        |
| --------- | -------- | -------- | ------- | ------------------ |
| `KEY`     | argument | ✅       | —       | A valid sector key |

**Examples:**

```bash
yfin sector-top-companies technology
yfin sector-top-companies consumer-cyclical
```

---

### `sector-top-etfs`

Get the top ETFs for a sector.

| Parameter | Type     | Required | Default | Description        |
| --------- | -------- | -------- | ------- | ------------------ |
| `KEY`     | argument | ✅       | —       | A valid sector key |

**Examples:**

```bash
yfin sector-top-etfs technology
yfin sector-top-etfs energy
```

---

### `sector-top-mutual-funds`

Get the top mutual funds for a sector.

| Parameter | Type     | Required | Default | Description        |
| --------- | -------- | -------- | ------- | ------------------ |
| `KEY`     | argument | ✅       | —       | A valid sector key |

**Examples:**

```bash
yfin sector-top-mutual-funds healthcare
```

---

## Industry

### `industry-overview`

Get overview information for an industry.

| Parameter | Type     | Required | Default | Description                                                              |
| --------- | -------- | -------- | ------- | ------------------------------------------------------------------------ |
| `KEY`     | argument | ✅       | —       | A valid industry key (use `yfin sector-industries <sector-key>` to find) |

**Examples:**

```bash
yfin industry-overview semiconductors
yfin industry-overview software-application
```

---

### `industry-research-reports`

Get research reports related to an industry.

| Parameter | Type     | Required | Default | Description          |
| --------- | -------- | -------- | ------- | -------------------- |
| `KEY`     | argument | ✅       | —       | A valid industry key |

**Examples:**

```bash
yfin industry-research-reports biotechnology
```

---

### `industry-top-companies`

Get the top companies within an industry.

| Parameter | Type     | Required | Default | Description          |
| --------- | -------- | -------- | ------- | -------------------- |
| `KEY`     | argument | ✅       | —       | A valid industry key |

**Examples:**

```bash
yfin industry-top-companies semiconductors
yfin industry-top-companies internet-retail
```

---

### `industry-top-growth-companies`

Get the top growth companies in an industry.

| Parameter | Type     | Required | Default | Description          |
| --------- | -------- | -------- | ------- | -------------------- |
| `KEY`     | argument | ✅       | —       | A valid industry key |

**Examples:**

```bash
yfin industry-top-growth-companies software-infrastructure
```

---

### `industry-top-performing-companies`

Get the top performing companies in an industry.

| Parameter | Type     | Required | Default | Description          |
| --------- | -------- | -------- | ------- | -------------------- |
| `KEY`     | argument | ✅       | —       | A valid industry key |

**Examples:**

```bash
yfin industry-top-performing-companies auto-manufacturers
```

---

## Screen

### `screen`

Run a stock screener. Supports predefined queries, simple filters (implicitly ANDed), or complex JSON queries.

| Parameter      | Type   | Required | Default | Description                                                                     |
| -------------- | ------ | -------- | ------- | ------------------------------------------------------------------------------- |
| `--filter`     | option | ✅\*     | —       | Filter in `<field> <operator> <value>` format. Can be specified multiple times. |
| `--predefined` | option | ✅\*     | —       | Predefined query name (use `yfin screen-predefined-queries` to list)            |
| `--json-query` | option | ✅\*     | —       | Complex query in JSON format                                                    |
| `--limit`      | option | —        | `12`    | Maximum number of results                                                       |
| `--offset`     | option | —        | `0`     | Offset for pagination                                                           |
| `--sort-field` | option | —        | —       | Field to sort results by (use `yfin screen-query-fields` to list)               |
| `--sort-order` | option | —        | `desc`  | Sort order: `asc` or `desc`                                                     |

> \*Exactly one of `--filter`, `--predefined`, or `--json-query` must be specified. They are mutually exclusive.

**Operators:** `eq`, `gt`, `gte`, `lt`, `lte`, `btwn`, `is-in`

**Examples:**

```bash
# Simple filter: Technology stocks
yfin screen --filter "sector eq Technology"

# Multiple filters (implicitly ANDed)
yfin screen --filter "sector eq Technology" --filter "region eq us"

# Using a predefined query
yfin screen --predefined most_actives

# Complex JSON query (AND/OR logic)
yfin screen --json-query '{"operator": "and", "queries": [{"operator": "or", "queries": ["sector eq Technology", "sector eq Healthcare"]}, "region eq us"]}'

# Sort by market cap, ascending
yfin screen --filter "region eq us" --sort-field "intradaymarketcap" --sort-order asc

# Get 25 results with offset
yfin screen --predefined day_gainers --limit 25 --offset 0

# Between filter (e.g., PE ratio between 10 and 20)
yfin screen --filter "peratio.lasttwelvemonths btwn 10,20"
```

---

### `screen-query-fields`

Get a list of all valid fields that can be used for screening.

| Parameter | Type | Required | Default | Description            |
| --------- | ---- | -------- | ------- | ---------------------- |
| _(none)_  | —    | —        | —       | No parameters required |

**Examples:**

```bash
yfin screen-query-fields
```

---

### `screen-query-values`

Get a list of all valid values for a given field.

| Parameter | Type   | Required | Default | Description                                                                       |
| --------- | ------ | -------- | ------- | --------------------------------------------------------------------------------- |
| `--field` | option | ✅       | —       | Field to get values for: `region`, `exchange`, `sector`, `industry`, `peer_group` |

**Examples:**

```bash
# List all valid regions
yfin screen-query-values --field region

# List all valid sectors
yfin screen-query-values --field sector

# List all valid exchanges
yfin screen-query-values --field exchange

# List all valid industries
yfin screen-query-values --field industry
```

---

### `screen-predefined-queries`

Get a list of all available predefined screening queries.

| Parameter | Type | Required | Default | Description            |
| --------- | ---- | -------- | ------- | ---------------------- |
| _(none)_  | —    | —        | —       | No parameters required |

**Examples:**

```bash
yfin screen-predefined-queries
```
