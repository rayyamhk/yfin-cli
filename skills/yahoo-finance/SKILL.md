---
name: yahoo-finance
description: Look up live and historical market data from Yahoo Finance with the `yfin` CLI — prices for stocks, ETFs, indices, crypto, FX and futures; company profile and valuation; income statement, balance sheet and cash flow; earnings dates and surprises; analyst ratings, price targets and estimates; insider and institutional holders; news; sector and industry rankings; and a stock screener. Use this whenever the user names a ticker or company and wants numbers about it, asks how a stock or the market is doing, wants to compare companies, check earnings, dividends or analyst sentiment, or find stocks matching criteria — even if they never say "Yahoo Finance".
---

# Yahoo Finance

`yfin` wraps Yahoo Finance in one command per dataset. Every command prints JSON, so read the numbers from it rather than from memory: market data changes daily and your training data is stale.

## Prerequisites

Assume `yfin` is installed. If a command fails with "command not found", install it (any one works) and retry:

```bash
uv tool install yfin-cli
# or
pipx install yfin-cli
```

## Pick the command from the question

Most questions need one or two calls. Start with the cheapest command that answers it.

| The user wants…                                    | Run                                                                    |
| -------------------------------------------------- | ---------------------------------------------------------------------- |
| Current price, day move, market cap, 52-week range | `fast-info T` (~0.5 KB)                                                |
| Valuation (P/E, P/B, EV/EBITDA), margins, beta, business summary, dividend yield | `info T` (~9 KB, so only when you need these fields) |
| Price over time, returns, charts                   | `history T --period 1y` (or `--start/--end`, `--interval 1wk`)         |
| Dividend payments                                  | `dividends T --period 5y`                                              |
| Revenue, profit, debt, cash, free cash flow        | `income-stmt`, `balance-sheet`, `cashflow` (`--frequency quarterly`)   |
| Next earnings date, or did they beat?              | `earnings-dates T` (next date + recent surprises), `earnings-history T` |
| Analyst view                                       | `recommendations`, `price-targets`, `upgrades-downgrades`              |
| Forward estimates                                  | `earnings-estimate`, `revenue-estimate`, `eps-trend`, `growth-estimates` |
| Who owns it, insider buying/selling                | `major-holders`, `institutional-holders`, `insider-transactions`       |
| Why did it move?                                   | `news T`, plus `upgrades-downgrades T` for recent rating changes       |
| Find stocks matching criteria                      | `screen` (read "Screening" below first)                                |
| What reports this week / IPOs / macro data         | `calendar-earnings`, `calendar-ipo`, `calendar-economic-events`        |
| Biggest companies or ETFs in a sector or industry  | `sector-top-companies KEY`, `industry-top-companies KEY`               |
| Is the US market open?                             | `market-status`                                                        |

Each command takes one ticker. To compare several, run the command once per ticker (a shell loop is fine) and put the numbers side by side.

Full options for every command are in the references; open the one you need:

| Category   | Commands                                                                                    | Reference                  |
| ---------- | ------------------------------------------------------------------------------------------- | -------------------------- |
| Stock      | `history`, `dividends`, `fast-info`, `info`, `news`, `market-status`                        | `references/stock.md`      |
| Calendar   | `calendar-earnings`, `calendar-economic-events`, `calendar-ipo`                             | `references/calendar.md`   |
| Financials | `income-stmt`, `balance-sheet`, `cashflow`, `earnings-dates`, `sec-filings`                 | `references/financials.md` |
| Analysis   | `recommendations`, `upgrades-downgrades`, `price-targets`, `earnings-estimate`, `revenue-estimate`, `earnings-history`, `eps-trend`, `eps-revisions`, `growth-estimates`, `insider-*`, `major-holders`, `institutional-holders`, `mutualfund-holders` | `references/analysis.md` |
| Screen     | `screen`, `screen-query-fields`, `screen-query-values`, `screen-predefined-queries`         | `references/screen.md`     |
| Sector     | `sector-keys`, `sector-industries`, `sector-overview`, `sector-top-*`, `sector-research-reports` | `references/sector.md` |
| Industry   | `industry-overview`, `industry-top-*`, `industry-research-reports`                          | `references/industry.md`   |

## Ticker symbols

Yahoo symbols are not always the plain ticker:

| Asset                 | Format             | Examples                      |
| --------------------- | ------------------ | ----------------------------- |
| US stock / ETF        | plain              | `AAPL`, `SPY`, `BRK-B` (dash, not dot) |
| Non-US stock          | ticker + exchange suffix | `7203.T` (Tokyo), `VOD.L` (London), `0700.HK`, `SAP.DE`, `RY.TO` |
| Index                 | `^` prefix         | `^GSPC` (S&P 500), `^IXIC`, `^DJI`, `^VIX` |
| Crypto                | `-USD` suffix      | `BTC-USD`, `ETH-USD`          |
| Currency pair         | `=X` suffix        | `EURUSD=X`, `JPY=X`           |
| Futures               | `=F` suffix        | `CL=F` (crude), `GC=F` (gold) |

Statements, analyst data and holders exist only for companies; for indices, crypto, FX and futures use `history` and `fast-info`.

## Screening

`screen` searches Yahoo's whole global database, and with no sort it returns results in reverse ticker order. A bare `--filter "sector eq Technology"` therefore returns obscure foreign listings with zero volume, not Apple and Microsoft. To get results a person would recognise, give every screen:

1. **A region**: `region eq us` (values are lowercase country codes).
2. **A size or liquidity floor**: e.g. `intradaymarketcap gt 2000000000` and `avgdailyvol3m gt 500000`. The volume floor also drops preferred shares (`JPM-PC`) and thin OTC listings.
3. **A sort**: `--sort-field intradaymarketcap` (or the metric the user cares about) with `--sort-order desc`.

Add `exchange is-in NMS,NYQ` (Nasdaq, NYSE) to keep only main-board US listings. Note that `region eq us` includes US-listed ADRs of foreign companies (e.g. `TTE`, `NVO`); say so if it matters to the user.

```bash
# Large US dividend payers yielding over 4%, biggest first
yfin screen --filter "region eq us" --filter "intradaymarketcap gt 10000000000" \
  --filter "avgdailyvol3m gt 500000" --filter "forward_dividend_yield gt 4" \
  --sort-field intradaymarketcap --limit 10

# OR logic needs --json-query
yfin screen --json-query '{"operator":"and","queries":["region eq us","exchange is-in NMS,NYQ","intradaymarketcap gt 2000000000",{"operator":"or","queries":["sector eq Technology","sector eq Healthcare"]}]}' --sort-field percentchange --limit 10
```

Things that trip people up:

- **Filter thresholds are in percent**, not fractions: `forward_dividend_yield gt 4` means 4%, `returnonequity.lasttwelvemonths gt 15` means 15%, `percentchange gt 5` means up 5% today.
- **Filter fields and result fields have different names.** You filter on `intradaymarketcap` and `peratio.lasttwelvemonths`; the results call them `marketCap` and `trailingPE`. The filter field list is in `references/screen.md`.
- **Categorical values are exact and case-sensitive.** The screener wants `sector eq Technology`; the `sector-*` commands want the key `technology`. When unsure, list them: `yfin screen-query-values --field sector` (also `industry`, `exchange`, `region`).
- For a quick standard list (`day_gainers`, `most_actives`, `undervalued_large_caps`, …) use `--predefined`; `yfin screen-predefined-queries` lists them.

## Reading the output

### Success, empty results, and errors

- **Success**: exit code `0`, JSON on stdout (a list of objects, or one object).
- **Empty list `[]`**: the ticker exists but has no data of that kind (e.g. `income-stmt` for an ETF). It is not an error.
- **Error**: exit code `1`, nothing on stdout, and one JSON line on stderr:

  ```json
  {"error": "not_found", "message": "Ticker 'XYZ' not found on Yahoo Finance"}
  ```

  | `error`     | Meaning                                                                           |
  | ----------- | --------------------------------------------------------------------------------- |
  | `not_found` | The ticker doesn't exist (or is delisted). Check the symbol format above.         |
  | `no_data`   | Nothing returned; for sector/industry commands the key is likely wrong (the message says how to list valid keys). |
  | `error`     | Anything else (network, Yahoo outage, rate limit). Retrying may help.             |

- **Invalid arguments**: exit code `2` with a usage message on stderr that names the bad option or value.

### Output size

Output is compact JSON, trimmed to save context:

- **Fields with no value are omitted** rather than set to `null`. A missing field means Yahoo has no value for it.
- **Long histories are capped at the 20 most recent rows**: `upgrades-downgrades`, `insider-transactions`, `sec-filings`. Use `--limit N` (or `--limit 0` for all) and `--offset N` to see more.
- **`screen` returns 19 summary fields per result** (price, change, volume, market cap, P/E, EPS, dividend yield, 52-week range, analyst rating). Use `--fields a,b,c` for specific fields, or `--all-fields` for all ~90.
- **`history`** omits `Dividends`/`Stock Splits` columns when there were none in the range.
- Numbers are rounded to 7 significant digits; values of 1,000,000 or more are whole numbers.

### Dates and freshness

- Daily or longer data uses the **exchange's local date**, as `YYYY-MM-DD` (a Tokyo bar for Nov 6 is `2026-11-06`).
- Timestamps keep their time and **UTC offset** (e.g. `2026-11-11T09:30:00-05:00`). Timestamps without an offset are as Yahoo provides them.
- Quotes are delayed about 15 minutes. When you report a price, give the date (and time, if intraday) it is from, so the user knows how fresh it is.

### Percentages: check the units

Yahoo mixes two conventions, sometimes for the same quantity. Before reporting a percentage, check which one the field uses.

**Fractions** (`0.0663` means 6.63%): this is the default for ratios, e.g. `pctHeld`, `pctChange`, `heldPercentInsiders`, `heldPercentInstitutions`, `shortPercentOfFloat`, `payoutRatio`, `profitMargins`, `grossMargins`, `revenueGrowth`, `earningsGrowth`, `52WeekChange`, `trailingAnnualDividendYield`, `ytd return`, `market weight`, `growth`, `stockTrend`/`indexTrend`, and `surprisePercent` in `earnings-history`. Values in `major-holders` are fractions too, except `institutionsCount`.

**Already percentages** (`5.8` means 5.8%):

| Command(s)              | Fields                                                     |
| ----------------------- | ---------------------------------------------------------- |
| `earnings-dates`        | `Surprise(%)`                                              |
| `info`, `screen`        | `dividendYield`, `fiveYearAvgDividendYield`                |
| `info`, `screen`        | `regularMarketChangePercent`, `fiftyTwoWeekChangePercent`  |
| `screen` filters        | every percentage threshold (see "Screening")               |

For example, the same quarter's earnings surprise is `5.8` in `earnings-dates` but `0.058` in `earnings-history`.
