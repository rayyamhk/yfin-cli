# Stock

## `history`

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

## `dividends`

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

## `fast-info`

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

### `info`

Get detailed info for a stock ticker. Returns comprehensive information including company profile, financial metrics, and market data.

| Parameter | Type     | Required | Default | Description         |
| --------- | -------- | -------- | ------- | ------------------- |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol |

**Examples:**

```bash
# Get detailed info for Tesla
yfin info TSLA
```

---

## `news`

Get news articles for a stock ticker.

| Parameter | Type     | Required | Default | Description                                      |
| --------- | -------- | -------- | ------- | ------------------------------------------------ |
| `TICKER`  | argument | ✅       | —       | Stock ticker symbol                              |
| `--count` | option   | —        | `5`     | Number of results to show                        |
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

## `market-status`

Get the current US market status (open/closed, trading hours, timezone).

| Parameter | Type | Required | Default | Description            |
| --------- | ---- | -------- | ------- | ---------------------- |
| _(none)_  | —    | —        | —       | No parameters required |

**Examples:**

```bash
# Check if the US market is open
yfin market-status
```
