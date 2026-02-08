import typer
from functools import wraps
from .writer import WriterFactory
from .validator import validate_data_frame_has_data
from .utils import print_error


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
        data_frame = func(*args, **kwargs)
        validate_data_frame_has_data(data_frame)
        output_type = kwargs.get("output")
        writer = WriterFactory.get_writer(output_type)
        writer.write_dataframe(data_frame)

    return wrapper
