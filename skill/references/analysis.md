# Analysis

## `recommendations`

Get analyst recommendations — number of buy, sell, and hold ratings across time periods.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin recommendations AAPL
yfin recommendations TSLA
```

---

## `upgrades-downgrades`

Get the history of analyst upgrades and downgrades.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin upgrades-downgrades AAPL
```

---

## `price-targets`

Get analyst price targets (current, low, high, mean, median).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin price-targets TSLA
```

---

## `earnings-estimate`

Get analyst earnings estimates for upcoming periods.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin earnings-estimate AAPL
```

---

## `revenue-estimate`

Get analyst revenue estimates for upcoming periods.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin revenue-estimate MSFT
```

---

## `earnings-history`

Get historical earnings — actual vs. estimated EPS.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin earnings-history GOOG
```

---

## `eps-trend`

Get the EPS trend — how estimates have changed over time.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin eps-trend AAPL
```

---

## `eps-revisions`

Get EPS revisions — analyst estimate changes (up/down revisions).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin eps-revisions NVDA
```

---

## `growth-estimates`

Get analyst growth estimates for a stock.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin growth-estimates AMZN
```

---

## `insider-purchases`

Get insider purchase activity summary.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin insider-purchases AAPL
```

---

## `insider-transactions`

Get detailed insider transaction records (buys, sells, exercises).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin insider-transactions TSLA
```

---

## `insider-roster-holders`

Get the insider roster — list of insiders and their holdings.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin insider-roster-holders MSFT
```

---

## `major-holders`

Get major holders breakdown (% held by insiders, institutions, etc.).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin major-holders AAPL
```

---

## `institutional-holders`

Get the top institutional holders and their positions.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin institutional-holders GOOG
```

---

## `mutualfund-holders`

Get the top mutual fund holders and their positions.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `TICKER` | argument | ✅ | — | Stock ticker symbol |

**Examples:**

```bash
yfin mutualfund-holders MSFT
```