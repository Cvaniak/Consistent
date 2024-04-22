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
    json_file = file.with_name(f"comments_{file.stem}.json")

    extract_comments.main(file.name, file.name, json_file)
    print(f"{file.stem} extracted to {json_file}")
    print(f"Some stats could be shown here")


@app.command()
def join(file: BipFile):
    """
    Join comments with source file
    """
    json_file = file.with_name(f"comments_{file.stem}.json")
    if not json_file.exists():
        raise typer.BadParameter("File does not exist.")
    # TODO: Check if json file with comments is compatible for simple join
    # TODO: Prepare strategy for harder files
    join_comments.main(file.name, file.name, json_file)

    print(f"{file.stem} is joined with {json_file.stem}")
    print(f"Some stats could be shown here")


if __name__ == "__main__":
    app()
