import json
from typing import Protocol
from rich.table import Table
from .utils import console_print, is_number
from rich import box


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


class JsonWriter(OutputWriter):
    def write(self, data: dict | list) -> None:
        console_print(json.dumps(data, indent=2, default=str))

class TableWriter(OutputWriter):
    def write(self, data: dict | list) -> None:
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