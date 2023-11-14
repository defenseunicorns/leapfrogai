import click
import sys

from leapfrogai.errors import AppImportError
from leapfrogai.utils import import_app

@click.argument("app", envvar="LEAPFROGAI_APP")
@click.option(
    "--host",
    type=str,
    default="0.0.0.0",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=50051,
    help="Bind socket to this port. If 0, an available port will be picked.",
    show_default=True,
)
@click.command()
def cli(app: str, host: str, port: str):
    sys.path.insert(0, ".")
    """Leapfrog AI CLI"""
    app = import_app(app)
    app().serve()

    
if __name__ == "__main__":
    cli()  # pragma: no cover