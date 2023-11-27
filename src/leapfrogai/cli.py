import click
import sys
import asyncio

from leapfrogai.utils import import_app
from leapfrogai.serve import serve

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
@click.option(
    "--app-dir",
    type=str,
    default="",
    help="Path to the directory containing the app module. Defaults to the current directory.",
    show_default=True,
)
@click.command()
def cli(app: str, host: str, port: str, app_dir: str):
    sys.path.insert(0, app_dir)
    """Leapfrog AI CLI"""
    app = import_app(app)
    asyncio.run(serve(app(), host, port))

    
if __name__ == "__main__":
    cli()  # pragma: no cover