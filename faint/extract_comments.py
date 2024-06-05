import bisect
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from tree_sitter import Node

from faint.utils import get_commit_sha, get_lines_hash, get_tree


@dataclass
class Position:
    row: int
    column: int


@dataclass
class Comment:
    start: Position
    text: str
    is_inline: bool


@dataclass
class FileMetadata:
    commit_sha: str
    file_name: str
    file_sha: str


@dataclass
class CommentsStruct:
    comments: List[Comment]
    deleted_lines: List[int]
    file_metadata: Optional[FileMetadata] = None


def collect_comment_nodes(tree):
    comment_nodes = []

    def _collect_comment_ranges(node: Node):
        if node.type == "comment":
            comment_nodes.append(node)
        else:
            for child in node.children:
                _collect_comment_ranges(child)

    _collect_comment_ranges(tree.root_node)

    return comment_nodes


def remove_comments(tree, lines):
    # Collect ranges for comments
    comment_nodes = collect_comment_nodes(tree)

    comments = []
    deleted_lines = []

    # Remove comments by replacing them with spaces (to preserve formatting)
    for node in reversed(comment_nodes):  # Reverse to avoid offset issues
        start_p, end_p = node.start_point, node.end_point
        is_inline = False
        text = lines[start_p[0]][start_p[1] : end_p[1]]

        # TODO: here was edge case, needs to be watched for more
        if (node.parent.start_point[0] != start_p[0] and node.prev_sibling.start_point[0] != start_p[0]) or (
            node.prev_sibling is None
        ):
            lines[start_p[0]] = ""
            bisect.insort(deleted_lines, start_p[0])
        else:
            lines[start_p[0]] = lines[start_p[0]][: start_p[1]].rstrip() + "\n"
            is_inline = True

        comment = Comment(
            start=Position(*start_p),
            text=text,
            is_inline=is_inline,
        )
        comments.append(comment)

    lines = [x for x in lines if x != ""]

    return comments, deleted_lines, lines


def extract_comments(input_file_path, source_code, lines):
    tree = get_tree(source_code)
    comments, deleted_lines, new_lines = remove_comments(tree, lines)

    metadata = FileMetadata(get_commit_sha(), input_file_path, get_lines_hash(lines))

    out_data = CommentsStruct(comments, deleted_lines, metadata)

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
