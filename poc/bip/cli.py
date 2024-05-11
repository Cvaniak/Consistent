from typing import Annotated
import typer
from pathlib import Path

from bip.utils import get_tree
from bip import extract_comments
from bip import join_comments

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

    extract_comments.main(file.absolute(), file.absolute(), json_file)
    print(f"{file.stem} extracted to {json_file}")
    print("Some stats could be shown here")


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
    join_comments.main(file.absolute(), file.absolute(), json_file)

    print(f"{file.stem} is joined with {json_file.stem}")
    print("Some stats could be shown here")


@app.command()
def list_comments(file: BipFile):
    """
    List all comments existing in code
    """
    with open(file, "r", encoding="utf-8") as f:
        source_code = f.read()
    tree = get_tree(source_code)

    comment_nodes = extract_comments.collect_comment_nodes(tree)

    for comment in comment_nodes:
        print(f"line {comment.start_point[0]}:\n{comment.text.decode('utf8')}")


if __name__ == "__main__":
    app()
