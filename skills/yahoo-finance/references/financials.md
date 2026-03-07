# Financials

## `income-stmt`

Get the income statement for a ticker.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |
| `--frequency` | option | — | `yearly` | Frequency: `yearly`, `quarterly`, `trailing` |

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

## `balance-sheet`

Get the balance sheet for a ticker.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |
| `--frequency` | option | — | `yearly` | Frequency: `yearly`, `quarterly` |

**Examples:**

```bash
# Get annual balance sheet
yfin balance-sheet AAPL

# Get quarterly balance sheet
yfin balance-sheet TSLA --frequency quarterly
```

---

## `cashflow`

Get the cash flow statement for a ticker.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |
| `--frequency` | option | — | `yearly` | Frequency: `yearly`, `quarterly`, `trailing` |

**Examples:**

```bash
# Get annual cash flow
yfin cashflow AAPL

# Get quarterly cash flow
yfin cashflow NVDA --frequency quarterly
```

---

## `earnings-dates`

Get earnings dates, estimates, and reported EPS for a ticker.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |
| `--limit` | option | — | `12` | Maximum number of results |
| `--offset` | option | — | `0` | Offset for pagination |

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

## `sec-filings`

Get SEC filings for a ticker.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
# Get SEC filings for Apple
yfin sec-filings AAPL
```