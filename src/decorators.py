import json
import logging
import sys
from functools import wraps
from typing import NoReturn

import typer
import yfinance as yf

from .typer import default_output
from .utils import console_print_error
from .writer import WriterFactory

# yfinance logs raw HTTP errors and "possibly delisted" guesses to stderr. The
# CLI reports its own errors instead, so stderr stays readable for agents.
logging.getLogger("yfinance").disabled = True

# Global options set by the app callback before any command runs. Kept here
# rather than on the click context because newer Typer versions vendor click
# and no longer expose click.get_current_context().
_settings = {"output": default_output}


def set_output_format(output: str) -> None:
    _settings["output"] = output


def ticker_exists(ticker: str) -> bool:
    """Whether Yahoo Finance knows this symbol.

    Costs one request, so it's only used after a command came back empty or
    failed, to tell "no such ticker" apart from "no data for this ticker".
    """
    try:
        return bool(yf.Ticker(ticker).get_history_metadata().get("symbol"))
    except Exception:
        return True  # Can't tell; don't claim the ticker is missing.


def _is_empty(data) -> bool:
    if data is None:
        return True
    if isinstance(data, (list, dict)) and not data:
        return True
    # e.g. `info` for an unknown symbol returns {"trailingPegRatio": None}
    return isinstance(data, dict) and all(v is None for v in data.values())


def _fail(code: str, message: str) -> NoReturn:
    """Report an error on stderr and exit 1. JSON output mode gets JSON errors."""
    if _settings["output"] == "json":
        print(json.dumps({"error": code, "message": message}), file=sys.stderr)
    else:
        console_print_error(message)
    raise typer.Exit(code=1)


def _not_found(ticker: str) -> NoReturn:
    _fail("not_found", f"Ticker '{ticker}' not found on Yahoo Finance")


def _no_data_message(func_name: str, key: str | None) -> str:
    if key is None:
        return "No data found"
    if func_name.startswith("sector"):
        hint = "List valid sector keys with `yfin sector-keys`."
    else:
        hint = "List valid industry keys with `yfin sector-industries <sector-key>`."
    return f"No data found for key '{key}'. {hint}"


def command(func):
    """Decorator to handle standard errors and output writing in CLI commands.

    Exit codes: 0 with JSON on stdout on success (possibly an empty list),
    1 with an error on stderr otherwise, 2 for invalid arguments.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        ticker = kwargs.get("ticker")
        try:
            data = func(*args, **kwargs)
        except (typer.Exit, typer.Abort, typer.BadParameter):
            raise
        except Exception as e:
            if ticker and not ticker_exists(ticker):
                _not_found(ticker)
            _fail("error", f"Unexpected error: {e}")

        if ticker and _is_empty(data) and not ticker_exists(ticker):
            _not_found(ticker)
        if data is None:
            _fail("no_data", _no_data_message(func.__name__, kwargs.get("key")))
        if not isinstance(data, (dict, list)):
            _fail(
                "error",
                f"Unexpected error: unsupported data type {type(data).__name__}",
            )

        WriterFactory.get_writer(_settings["output"]).write(data)

    return wrapper
