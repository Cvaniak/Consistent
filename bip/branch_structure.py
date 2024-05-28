import bisect
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

import git
from tree_sitter import Node, Tree
from utils import get_tree


@dataclass
class Position:
    row: int
    column: int


@dataclass
class Comment:
    start: Position
    text: str
    branch: list[str]


@dataclass
class CommentsStruct:
    comments: List[Comment]
    deleted_lines: List[int]
    commit_sha: str
    file_name: str


def collect_comment_nodes(tree: Tree):
    comment_nodes = []

    def _collect_comment_ranges(node: Node):
        if node.type == "comment":
            branch = []
            curr = node
            print(curr, tree.root_node)
            while curr is not None and curr != tree.root_node:
                print(curr)
                branch.append(str(curr.text, encoding="utf8"))
                # branch.append(curr.sexp)
                curr = curr.parent
            comment_nodes.append(
                (
                    Comment(
                        start=Position(*node.start_point),
                        text=str(node.text, encoding="utf-8"),
                        branch=branch,
                    ),
                    node,
                )
            )
        else:
            for child in node.children:
                _collect_comment_ranges(child)

    _collect_comment_ranges(tree.root_node)

    return comment_nodes


def remove_comments(tree, lines):
    # Collect ranges for comments
    comments_nodes: list[tuple[Comment, Node]] = collect_comment_nodes(tree)

    deleted_lines = []

    # Remove comments by replacing them with spaces (to preserve formatting)
    for comment, node in reversed(comments_nodes):  # Reverse to avoid offset issues
        start_p = comment.start

        # comment = Comment(
        #     start=Position(*start_p), text=lines[start_p[0]][start_p[1] : end_p[1]]
        # )

        # TODO: here was edge case, needs to be watched for more
        if (
            node.parent is not None
            and node.parent.start_point[0] != start_p.row
            and node.prev_sibling is not None
            and node.prev_sibling.start_point[0] != start_p.row
        ) or (node.prev_sibling is None):
            lines[start_p.row] = ""
            bisect.insort(deleted_lines, start_p.row)
        else:
            lines[start_p.row] = lines[start_p.row][: start_p.column].rstrip() + "\n"

    lines = [x for x in lines if x != ""]

    return [comment for comment, _ in reversed(comments_nodes)], deleted_lines, lines


def get_commit_sha():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return sha


def extract_comments(input_file_path, source_code, lines):
    tree = get_tree(source_code)
    comments, deleted_lines, new_lines = remove_comments(tree, lines)

    out_data = CommentsStruct(comments, deleted_lines, get_commit_sha(), input_file_path)

    return new_lines, out_data


# Example of reading,
# processing, and writing the file
# also three line comment
def main(input_file_path: Path, output_file_path: Path, output_comments_file_path: Path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    with open(input_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    new_lines, out_data = extract_comments(str(input_file_path), source_code, lines)

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(new_lines)

    with open(output_comments_file_path, "w", encoding="utf-8") as file:
        json.dump(asdict(out_data), file, indent=4)


if __name__ == "__main__":
    input_file_path = Path("./tests/cases/happy_path/with_comments.py")
    output_file_path = Path("./tests/cases/happy_path/no_comments.py")
    output_comments_file_path = Path("./tests/cases/happy_path/comments.json")
    main(input_file_path, output_file_path, output_comments_file_path)
