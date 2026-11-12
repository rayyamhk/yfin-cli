import json
import math
import sys
from typing import Any, Protocol
from rich.table import Table
from .utils import console_print


class OutputWriter(Protocol):
    def write(self, data: dict | list) -> None: ...


class WriterFactory:
    @staticmethod
    def get_writer(writer_type: str) -> OutputWriter:
        if writer_type == "json":
            return JsonWriter()
        if writer_type == "table":
            return TableWriter()
        raise ValueError(f"Unsupported writer type: {writer_type}")


def _clean_number(value: float) -> int | float | None:
    """Drop float noise: 395.42999267578125 -> 395.43, 838588.0 -> 838588.

    Keeps 7 significant digits, which removes float32 artifacts without
    losing real precision (small prices like 0.0000123456 survive). Values of
    a million or more (market caps, volumes, revenue) become integers.
    NaN/Infinity become None, since they aren't valid JSON.
    """
    if not math.isfinite(value):
        return None
    if value.is_integer() or abs(value) >= 1e6:
        return int(round(value))
    return float(f"{value:.7g}")


def simplify(data: Any, drop_nulls: bool) -> Any:
    """Clean numbers everywhere and optionally drop null fields from objects."""
    if isinstance(data, dict):
        cleaned = {k: simplify(v, drop_nulls) for k, v in data.items()}
        if drop_nulls:
            cleaned = {k: v for k, v in cleaned.items() if v is not None}
        return cleaned
    if isinstance(data, list):
        return [simplify(v, drop_nulls) for v in data]
    if isinstance(data, float):
        return _clean_number(data)
    return data


class JsonWriter(OutputWriter):
    """Pretty JSON in a terminal; compact JSON when piped (agents, scripts),
    which saves ~20% of tokens. Fields with no value are omitted."""

    def write(self, data: dict | list) -> None:
        data = simplify(data, drop_nulls=True)
        if sys.stdout.isatty():
            text = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        else:
            text = json.dumps(
                data, separators=(",", ":"), ensure_ascii=False, default=str
            )
        # Use print() instead of console_print() because Rich interprets
        # escape sequences and markup, corrupting JSON with special characters.
        print(text)


class TableWriter(OutputWriter):
    def write(self, data: dict | list) -> None:
        data = simplify(data, drop_nulls=False)
        table = Table(header_style="bold cyan")

        if isinstance(data, dict):
            data = [data]

        if len(data) == 0:
            console_print(table)
            return

        for key, value in data[0].items():
            table.add_column(key)

        for record in data:
            table.add_row(*[str(value) for value in record.values()])

        console_print(table)
