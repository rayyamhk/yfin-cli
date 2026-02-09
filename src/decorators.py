import typer
import click
from functools import wraps
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
        ctx = click.get_current_context()
        output_type = ctx.obj.get("output")
        writer = WriterFactory.get_writer(output_type)

        if not isinstance(data, (dict, list)):
            raise ValueError(f"Unsupported data type: {type(data)}")

        if not data:
            print_warning("No data found")
            raise typer.Exit(code=1)

        writer.write(data)

    return wrapper
