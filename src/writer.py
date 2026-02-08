from typing import Protocol
from pandas import DataFrame, RangeIndex
from .utils import print


class OutputWriter(Protocol):
    def write_dataframe(self, data: DataFrame) -> None: ...
    def write_list(self, data: list) -> None: ...
    def write_dict(self, data: dict) -> None: ...


class WriterFactory:
    @staticmethod
    def get_writer(writer_type: str) -> OutputWriter:
        if writer_type == "raw":
            return RawWriter()
        if writer_type == "table":
            return TableWriter()
        raise ValueError(f"Unsupported writer type: {writer_type}")


class RawWriter(OutputWriter):
    def write_dataframe(self, data: DataFrame) -> None:
        print(data)

    def write_list(self, data: list) -> None:
        print(data)

    def write_dict(self, data: dict) -> None:
        print(data)


# TODO: fix table writer
class TableWriter(OutputWriter):
    def write_dataframe(self, data: DataFrame) -> None:
        if isinstance(data.index, RangeIndex):
            print(data.to_string(index=False))
        else:
            print(data)

    def write_list(self, data: list) -> None:
        self.write_dataframe(DataFrame(data))

    def write_dict(self, data: dict) -> None:
        data_frame = DataFrame(list(data.items()))
        self.write_dataframe(data_frame)
