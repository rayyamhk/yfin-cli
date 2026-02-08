from typing import Protocol, Any
from pandas import DataFrame, RangeIndex
from .utils import print


class OutputWriter(Protocol):
    def write_dataframe(self, data: DataFrame, **kwargs: Any) -> None: ...


class WriterFactory:
    @staticmethod
    def get_writer(writer_type: str) -> OutputWriter:
        if writer_type == "table":
            return TableWriter()
        raise ValueError(f"Unsupported writer type: {writer_type}")


class TableWriter(OutputWriter):
    def write_dataframe(self, data: DataFrame, **kwargs: Any) -> None:
        if isinstance(data.index, RangeIndex):
            print(data.to_string(index=False))
        else:
            print(data)
