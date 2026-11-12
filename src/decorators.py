import typer
from functools import wraps
from .writer import WriterFactory
from .utils import console_print_error, console_print_warning
from .typer import default_output

# Global options set by the app callback before any command runs. Kept here
# rather than on the click context because newer Typer versions vendor click
# and no longer expose click.get_current_context().
_settings = {"output": default_output}


def set_output_format(output: str) -> None:
    _settings["output"] = output


def command(func):
    """Decorator to handle standard errors and output writing in CLI commands."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)

            if data is None:
                console_print_warning("No data found")
                raise typer.Exit(code=1)

            if not isinstance(data, (dict, list)):
                raise ValueError(f"Unsupported data type: {type(data).__name__}")

            writer = WriterFactory.get_writer(_settings["output"])
            writer.write(data)
        except (typer.Exit, typer.Abort, typer.BadParameter):
            raise
        except Exception as e:
            console_print_error(f"Unexpected error: {e}")
            raise typer.Exit(code=1)

    return wrapper
