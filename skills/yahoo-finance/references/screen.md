**Examples:**

Without a region, a size floor and a sort, results come back in reverse ticker order from every exchange in the world (see "Screening" in SKILL.md). The examples below include all three.

```bash
# Largest US tech stocks
yfin screen --filter "sector eq Technology" --filter "region eq us" --sort-field intradaymarketcap --limit 10

# OR logic needs --json-query
yfin screen --json-query '{"operator": "and", "queries": [{"operator": "or", "queries": ["sector eq Technology", "sector eq Healthcare"]}, "region eq us", "intradaymarketcap gt 2000000000"]}' --sort-field intradaymarketcap

# Between filter: US large caps with P/E between 10 and 20
yfin screen --filter "region eq us" --filter "intradaymarketcap gt 10000000000" --filter "peratio.lasttwelvemonths btwn 10,20" --sort-field intradaymarketcap

# is-in filter: main US exchanges only
yfin screen --filter "exchange is-in NMS,NYQ" --filter "avgdailyvol3m gt 1000000" --sort-field dayvolume

# Using a predefined query (already scoped by Yahoo, no extra filters needed)
yfin screen --predefined most_actives --limit 25

# Next page
yfin screen --predefined day_gainers --limit 25 --offset 25

# Pick result fields, or get all ~90
yfin screen --predefined most_actives --fields "trailingPE,forwardPE,marketCap"
yfin screen --predefined most_actives --all-fields
```

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
| `--fields` | option | — | summary | Comma-separated result fields to return (`symbol` is always included) |
| `--all-fields` | flag | — | off | Return every field Yahoo provides (~90 per result) instead of the summary |

> \*Exactly one of `--filter`, `--predefined`, or `--json-query` must be specified. They are mutually exclusive.

**Operators:** `eq`, `gt`, `gte`, `lt`, `lte`, `btwn`, `is-in`

Each result includes a summary by default: `symbol`, `longName`, `quoteType`, `fullExchangeName`, `currency`, `regularMarketPrice`, `regularMarketChangePercent`, `regularMarketVolume`, `averageDailyVolume3Month`, `marketCap`, `trailingPE`, `forwardPE`, `epsTrailingTwelveMonths`, `priceToBook`, `dividendYield`, `fiftyTwoWeekLow`, `fiftyTwoWeekHigh`, `fiftyTwoWeekChangePercent`, `averageAnalystRating` (fields Yahoo has no value for are omitted).

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

# Pick result fields, or get all ~90
yfin screen --predefined most_actives --fields "trailingPE,forwardPE,marketCap"
yfin screen --predefined most_actives --all-fields
```

---

## `screen-query-fields`

Get a list of all valid fields that can be used for screening.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| *(none)* | — | — | — | No parameters required |

The same list, grouped, so you usually don't need to run it. Percent-type fields take thresholds in percent (`gt 15` = 15%). Fields ending in `.lasttwelvemonths` are trailing twelve months; money values are in the listing's currency.

| Group | Fields |
|-------|--------|
| Categorical | `region`, `exchange`, `sector`, `industry`, `peer_group` (values: `screen-query-values`) |
| Price & trading | `intradayprice`, `intradaypricechange`, `percentchange`, `eodprice`, `fiftytwowkpercentchange`, `lastclose52weekhigh.lasttwelvemonths`, `lastclose52weeklow.lasttwelvemonths`, `dayvolume`, `eodvolume`, `avgdailyvol3m`, `beta` |
| Size | `intradaymarketcap`, `lastclosemarketcap.lasttwelvemonths`, `totalsharesoutstanding`, `totalcommonsharesoutstanding.lasttwelvemonths` |
| Valuation | `peratio.lasttwelvemonths`, `lastclosepriceearnings.lasttwelvemonths`, `pegratio_5y`, `pricebookratio.quarterly`, `lastclosepricetangiblebookvalue.lasttwelvemonths`, `lastclosemarketcaptotalrevenue.lasttwelvemonths`, `lastclosetevtotalrevenue.lasttwelvemonths`, `lastclosetevebitda.lasttwelvemonths`, `lastclosetevebit.lasttwelvemonths` |
| Profitability | `grossprofitmargin.lasttwelvemonths`, `ebitdamargin.lasttwelvemonths`, `netincomemargin.lasttwelvemonths`, `returnonequity.lasttwelvemonths`, `returnonassets.lasttwelvemonths`, `returnontotalcapital.lasttwelvemonths` |
| Income & cash flow | `totalrevenues.lasttwelvemonths`, `grossprofit.lasttwelvemonths`, `ebitda.lasttwelvemonths`, `ebit.lasttwelvemonths`, `operatingincome.lasttwelvemonths`, `netincomeis.lasttwelvemonths`, `netepsbasic.lasttwelvemonths`, `netepsdiluted.lasttwelvemonths`, `basicepscontinuingoperations.lasttwelvemonths`, `dilutedepscontinuingoperations.lasttwelvemonths`, `cashfromoperations.lasttwelvemonths`, `capitalexpenditure.lasttwelvemonths`, `leveredfreecashflow.lasttwelvemonths`, `unleveredfreecashflow.lasttwelvemonths` |
| Growth | `totalrevenues1yrgrowth.lasttwelvemonths`, `quarterlyrevenuegrowth.quarterly`, `ebitda1yrgrowth.lasttwelvemonths`, `netincome1yrgrowth.lasttwelvemonths`, `epsgrowth.lasttwelvemonths`, `dilutedeps1yrgrowth.lasttwelvemonths`, `cashfromoperations1yrgrowth.lasttwelvemonths`, `leveredfreecashflow1yrgrowth.lasttwelvemonths` |
| Balance sheet & leverage | `totalassets.lasttwelvemonths`, `totalcurrentassets.lasttwelvemonths`, `totalcurrentliabilities.lasttwelvemonths`, `totalcashandshortterminvestments.lasttwelvemonths`, `totaldebt.lasttwelvemonths`, `totalequity.lasttwelvemonths`, `totalcommonequity.lasttwelvemonths`, `bookvalueshare.lasttwelvemonths`, `currentratio.lasttwelvemonths`, `quickratio.lasttwelvemonths`, `totaldebtequity.lasttwelvemonths`, `ltdebtequity.lasttwelvemonths`, `totaldebtebitda.lasttwelvemonths`, `netdebtebitda.lasttwelvemonths`, `ebitdainterestexpense.lasttwelvemonths`, `ebitinterestexpense.lasttwelvemonths`, `operatingcashflowtocurrentliabilities.lasttwelvemonths`, `altmanzscoreusingtheaveragestockinformationforaperiod.lasttwelvemonths` |
| Dividends | `dividendyield`, `forward_dividend_yield`, `forward_dividend_per_share`, `dividendpershare.lasttwelvemonths`, `consecutive_years_of_dividend_growth_count` |
| Ownership & short interest | `pctheldinsider`, `pctheldinst`, `short_interest.value`, `short_interest_percentage_change.value`, `short_percentage_of_float.value`, `short_percentage_of_shares_outstanding.value`, `days_to_cover_short.value` |
| ESG | `esg_score`, `environmental_score`, `social_score`, `governance_score`, `highest_controversy` |

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