import json
from typing import Protocol
from pandas import DataFrame
from .utils import print

class OutputWriter(Protocol):
    def write(self, data: dict | list) -> None: ...


class WriterFactory:
    @staticmethod
    def get_writer(writer_type: str) -> OutputWriter:
        if writer_type == "json":
            return JsonWriter()
        raise ValueError(f"Unsupported writer type: {writer_type}")


class JsonWriter(OutputWriter):
    def write(self, data: dict | list) -> None:
        print(json.dumps(data, indent=2, default=str))

