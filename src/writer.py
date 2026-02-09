from typing import Protocol
from pandas import DataFrame, RangeIndex
from .utils import print


class OutputWriter(Protocol):
    def write(self, data: dict) -> None: ...


class WriterFactory:
    @staticmethod
    def get_writer(writer_type: str) -> OutputWriter:
        if writer_type == "raw":
            return RawWriter()
        if writer_type == "table":
            return TableWriter()
        raise ValueError(f"Unsupported writer type: {writer_type}")


class RawWriter(OutputWriter):
    def write(self, data: dict) -> None:
        print(data)


# TODO: fix table writer
class TableWriter(OutputWriter):
    def write(self, data: dict) -> None:
        data_frame = DataFrame(list(data.items()))
        self.write_dataframe(data_frame)
