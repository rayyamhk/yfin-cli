# yfin-cli

A CLI wrapper for [yfinance](https://github.com/ranaroussi/yfinance).

## Features

- **Historical Data**: Get historical stock data with various intervals.
- **News**: Fetch latest news for a ticker.
- **Fast Info**: Quick summary of key stock metrics.
- **Calendars**:
  - Earnings Calendar (`yfin calendar-earnings`)
  - IPO Calendar (`yfin calendar-ipo`)
  - Economic Events (`yfin calendar-economic-events`)
- **Financial Statements**:
  - Income Statement (`yfin income-statement`)
  - Balance Sheet (`yfin balance-sheet`)
  - Cash Flow (`yfin cashflow`)
- **Earnings Dates**: Detailed earnings history and estimates (`yfin earnings-dates`).

## Installation

### Using uv (Recommended)

```bash
# Install directly from source
uv tool install .
```

### Using pip

```bash
pip install .
```

## Usage

```bash
yfin [OPTIONS] COMMAND [ARGS]...
```

### Examples

**Get Historical Data:**
```bash
yfin history AAPL --period 1y --interval 1d
```

**View Income Statement:**
```bash
yfin income-statement MSFT --quarterly
```

**Check Earnings Dates:**
```bash
yfin earnings-dates TSLA
```

**View Cash Flow (Trailing 12 Months):**
```bash
yfin cashflow NVDA --frequency trailing
```

**Get Recent News:**
```bash
yfin news GOOGL --limit 5
```

## Development

This project involves `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Build package
uv build
```
