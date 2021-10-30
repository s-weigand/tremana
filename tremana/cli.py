"""Console script for tremana."""
from __future__ import annotations

import sys

import click


@click.command()
def main(args: list[str] | None = None) -> int:
    """Console script for tremana.

    Parameters
    ----------
    args : List[str], optional
        Commandline arguments

    Returns
    -------
    int
    """
    click.echo("Replace this message by putting your code into " "tremana.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
