from pathlib import Path
from typing import Annotated

import typer

from faint import diff_trees, extract_comments, join_comments
from faint.utils import compare_files, get_tree

app = typer.Typer(no_args_is_help=True)

FaintFile = Annotated[
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
def extract(file: FaintFile):
    """
    Extract comments from choosen file
    """
    json_file = file.with_name(f"comments_{file.stem}.json")

    extract_comments.main(file.absolute(), file.absolute(), json_file)
    print(f"{file.stem} extracted to {json_file}")
    print("Some stats could be shown here")


@app.command()
def join(file: FaintFile):
    """
    Join comments with source file
    """
    json_file = file.with_name(f"comments_{file.stem}.json")
    if not json_file.exists():
        raise typer.BadParameter("File does not exist.")

    if compare_files(json_file, file):
        join_comments.main(file.absolute(), file.absolute(), json_file)
        print(f"{file.stem} is joined with {json_file.stem}")
        print("Some stats could be shown here")
    else:
        diff_trees.main_between_commits(file, json_file)
        print("Difficult case")


@app.command()
def list_comments(file: FaintFile):
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
