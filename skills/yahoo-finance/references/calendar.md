# Calendar

## `calendar-earnings`

Get the earnings calendar — upcoming and recent earnings announcements.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--start` | option | — | today | Start date (`YYYY-MM-DD`) |
| `--end` | option | — | today + 7 days | End date (`YYYY-MM-DD`) |
| `--limit` | option | — | `12` | Maximum number of results |
| `--offset` | option | — | `0` | Offset for pagination |
| `--market-cap` | option | — | `0` | Minimum market cap filter |

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

## `calendar-ipo`

Get the IPO calendar — upcoming initial public offerings.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--start` | option | — | today | Start date (`YYYY-MM-DD`) |
| `--end` | option | — | today + 7 days | End date (`YYYY-MM-DD`) |
| `--limit` | option | — | `12` | Maximum number of results |
| `--offset` | option | — | `0` | Offset for pagination |

**Examples:**

```bash
# Get upcoming IPOs this week
yfin calendar-ipo

# Get IPOs for next month
yfin calendar-ipo --start 2026-03-01 --end 2026-03-31
```

---

## `calendar-economic-events`

Get the economic events calendar — scheduled economic data releases and events.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--start` | option | — | today | Start date (`YYYY-MM-DD`) |
| `--end` | option | — | today + 7 days | End date (`YYYY-MM-DD`) |
| `--limit` | option | — | `12` | Maximum number of results |
| `--offset` | option | — | `0` | Offset for pagination |

**Examples:**

```bash
# Get this week's economic events
yfin calendar-economic-events

# Get events for a specific week with more results
yfin calendar-economic-events --start 2026-02-10 --end 2026-02-14 --limit 50
```