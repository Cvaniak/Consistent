from typing import Annotated
import typer
import extract_comments
import join_comments
from pathlib import Path

app = typer.Typer(no_args_is_help=True)

BipFile = Annotated[
    Path,
    typer.Argument(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
]


@app.command()
def extract(file: BipFile):
    """
    Extract comments from choosen file
    """
    extract_comments.main(file.name, file.name, "./def.json")


@app.command()
def join(file: BipFile):
    """
    Join comments with source file
    """
    # TODO: add json file as parameter
    # TODO: Check if json file exists
    # TODO: Check if json file with comments is compatible for simple join
    # TODO: Prepare strategy for harder files
    join_comments.main(file.name, file.name, "./def.json")


if __name__ == "__main__":
    app()
