import typer
from functools import wraps
from pandas import DataFrame, Series
from .writer import WriterFactory
from .utils import print_error, print_warning


def handle_errors(func):
    """Decorator to handle standard errors in CLI commands."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except typer.Exit, typer.Abort, typer.BadParameter:
            raise
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            raise typer.Exit(code=1)

    return wrapper


def with_output(func):
    """Decorator to handle output writing for CLI commands."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        output_type = kwargs.get("output")
        writer = WriterFactory.get_writer(output_type)

        has_data = True
        if isinstance(data, (DataFrame, Series)):
            if data.empty:
                has_data = False
            else:
                writer.write_dataframe(data)
        elif isinstance(data, list):
            if not data:
                has_data = False
            else:
                writer.write_list(data)
        elif isinstance(data, dict):
            if not data:
                has_data = False
            else:
                writer.write_dict(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

        if not has_data:
            print_warning("No data found")
            raise typer.Exit(code=1)

    return wrapper
