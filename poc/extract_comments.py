from dataclasses import dataclass, asdict
import json
from typing import List, Tuple
from tree_sitter import Language, Node, Parser
import git
import bisect


@dataclass
class Position:
    row: int
    column: int


@dataclass
class Comment:
    start: Position
    text: str


@dataclass
class CommentsStruct:
    comments: List[Comment]
    deleted_lines: List[int]
    commit_sha: str
    file_name: str


# Load the language library (Adjust the path to your compiled language library)
def get_tree(source_code):
    Language.build_library(
        "build/my-languages.so",
        ["tree-sitter-python"],  # Assuming the grammar files are correctly configured
    )

    PY_LANGUAGE = Language("build/my-languages.so", "python")
    parser = Parser()
    parser.set_language(PY_LANGUAGE)

    tree = parser.parse(bytes(source_code, "utf8"))
    return tree


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

        comment = Comment(
            start=Position(*start_p), text=lines[start_p[0]][start_p[1] : end_p[1]]
        )
        comments.append(comment)

        # TODO: here was edge case, needs to be watched for more
        if (
            node.parent.start_point[0] != start_p[0]
            and node.prev_sibling.start_point[0] != start_p[0]
        ) or node.parent.type == "module":
            lines[start_p[0]] = ""
            bisect.insort(deleted_lines, start_p[0])
        else:
            lines[start_p[0]] = lines[start_p[0]][: start_p[1]].rstrip() + "\n"

    lines = [x for x in lines if x != ""]

    return comments, deleted_lines, lines


def get_commit_sha():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return sha


def extract_comments(input_file_path, source_code, lines):
    tree = get_tree(source_code)
    comments, deleted_lines, new_lines = remove_comments(tree, lines)

    out_data = CommentsStruct(
        comments, deleted_lines, get_commit_sha(), input_file_path
    )

    return new_lines, out_data


# Example of reading,
# processing, and writing the file
# also three line comment
def main(input_file_path, output_file_path, output_comments_file_path):
    with open(input_file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    with open(input_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    new_lines, out_data = extract_comments(input_file_path, source_code, lines)

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(new_lines)

    with open(output_comments_file_path, "w", encoding="utf-8") as file:
        json.dump(asdict(out_data), file, indent=4)


if __name__ == "__main__":
    input_file_path = "extract_comments.py"
    output_file_path = "main_no_comments.py"
    output_comments_file_path = "just_comments.json"
    input_file_path = "./tests/cases/happy_path/with_comments.py"
    output_file_path = "./tests/cases/happy_path/no_comments.py"
    output_comments_file_path = "./tests/cases/happy_path/comments.json"
    main(input_file_path, output_file_path, output_comments_file_path)
