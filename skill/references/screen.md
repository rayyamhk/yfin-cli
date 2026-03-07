# Screen

## `screen`

Run a stock screener. Supports predefined queries, simple filters (implicitly ANDed), or complex JSON queries.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--filter` | option | ✅* | — | Filter in `<field> <operator> <value>` format. Can be specified multiple times. |
| `--predefined` | option | ✅* | — | Predefined query name (use `yfin screen-predefined-queries` to list) |
| `--json-query` | option | ✅* | — | Complex query in JSON format |
| `--limit` | option | — | `12` | Maximum number of results |
| `--offset` | option | — | `0` | Offset for pagination |
| `--sort-field` | option | — | — | Field to sort results by (use `yfin screen-query-fields` to list) |
| `--sort-order` | option | — | `desc` | Sort order: `asc` or `desc` |

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

## `screen-query-fields`

Get a list of all valid fields that can be used for screening.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| *(none)* | — | — | — | No parameters required |

**Examples:**

```bash
yfin screen-query-fields
```

---

## `screen-query-values`

Get a list of all valid values for a given field.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--field` | option | ✅ | — | Field to get values for: `region`, `exchange`, `sector`, `industry`, `peer_group` |

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

## `screen-predefined-queries`

Get a list of all available predefined screening queries.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| *(none)* | — | — | — | No parameters required |

**Examples:**

```bash
yfin screen-predefined-queries
```