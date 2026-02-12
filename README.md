# yfin-cli

A command-line interface for Yahoo Finance data, powered by [yfinance](https://github.com/ranaroussi/yfinance).

## Why yfin-cli

- Fast, scriptable access to Yahoo Finance data.
- JSON or table output for easy piping.
- Broad coverage: prices, financials, analyst data, screeners, sectors, industries.

## Install

Requires Python 3.10+.

### From PyPI (recommended)

```bash
pipx install yfin-cli
# or
pip install yfin-cli
# or
uv tool install yfin-cli
```

### From source

```bash
git clone <your-repo-url>
cd yfin-cli
uv tool install .
# or
pip install .
```

## Usage

### Quickstart

```bash
# Get historical stock data
yfin history AAPL

# Get quick summary metrics
yfin fast-info TSLA

# Check market status
yfin market-status

# View quarterly income statement
yfin income-stmt MSFT --frequency quarterly

# Get analyst recommendations
yfin recommendations NVDA

# Screen stocks
yfin screen --filter "sector eq Technology" --filter "intradaymarketcap gt 100000000000"

# Use a predefined screener
yfin screen --predefined day_gainers

# Output as a table
yfin --output table history AAPL --period 1y
```

> For the complete command reference with all options and parameters, see [COMMANDS.md](COMMANDS.md).

### Global options:

| Option     | Description                     | Default |
| ---------- | ------------------------------- | ------- |
| `--output` | Output format (`json`, `table`) | `json`  |
| `--help`   | Show help message               | —       |

## Available Commands

| Category       | Commands                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Stock**      | `history`, `dividends`, `fast-info`, `news`                                                                                                                              |
| **Market**     | `market-status`                                                                                                                                                          |
| **Calendar**   | `calendar-earnings`, `calendar-economic-events`, `calendar-ipo`                                                                                                          |
| **Financials** | `income-stmt`, `balance-sheet`, `cashflow`, `earnings-dates`, `sec-filings`                                                                                              |
| **Analysis**   | `recommendations`, `upgrades-downgrades`, `price-targets`, `earnings-estimate`, `revenue-estimate`, `earnings-history`, `eps-trend`, `eps-revisions`, `growth-estimates` |
| **Holders**    | `insider-purchases`, `insider-transactions`, `insider-roster-holders`, `major-holders`, `institutional-holders`, `mutualfund-holders`                                    |
| **Sector**     | `sector-keys`, `sector-industries`, `sector-overview`, `sector-research-reports`, `sector-top-companies`, `sector-top-etfs`, `sector-top-mutual-funds`                   |
| **Industry**   | `industry-overview`, `industry-research-reports`, `industry-top-companies`, `industry-top-growth-companies`, `industry-top-performing-companies`                         |
| **Screen**     | `screen`, `screen-query-fields`, `screen-query-values`, `screen-predefined-queries`                                                                                      |

## Development

This project uses uv for dependency management.

```bash
# Install dependencies
uv sync

# Run the CLI
uv run yfin --help

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Build package
uv build
```

## License

MIT
