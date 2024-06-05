import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, cast

from tree_sitter import Node, Parser

from faint.utils import get_file_bytes_by_commit_sha, load_language


@dataclass
class LeafNode:
    text: str
    line: int
    comment: bool = False
    marked: bool = False
    alone: bool = True
    node: Optional["LeafNode"] = None
    column: int = 0
    below_comment: Optional["LeafNode"] = None

    def __eq__(self, other):
        return self.text == other.text


@dataclass
class MissingComments:
    comment: LeafNode
    target_node: Optional[LeafNode] = None


def serialize_tree(node: Node, leaf_nodes: list[LeafNode]) -> None:
    # It contains children -> it is "leaf"
    if node.child_count > 0:
        for child in node.children:
            serialize_tree(child, leaf_nodes)

    else:
        x = LeafNode(node.text.decode("utf-8"), node.start_point[0], column=node.start_point[1])

        if node.type == "comment":
            x.comment = True
            if leaf_nodes:
                # If code is in the same line with comment
                if leaf_nodes[-1].line == x.line:
                    x.alone = False
                    x.node = leaf_nodes[-1]
                    leaf_nodes[-1].marked = True
                    leaf_nodes[-1].node = x

                # If previous node is also comment we group them
                elif leaf_nodes[-1].comment:
                    x.below_comment = leaf_nodes[-1]

        else:
            # if previous leaf is comment we mark this node and attach comment node
            if leaf_nodes and leaf_nodes[-1].comment and leaf_nodes[-1].alone:
                x.marked = True
                leaf_nodes[-1].node = x
                x.node = leaf_nodes[-1]

        leaf_nodes.append(x)


def get_serialized_tree_bytes(file: bytes, parser: Parser) -> list[LeafNode]:
    tree = parser.parse(file)

    serialized_tree: list[LeafNode] = []
    serialize_tree(tree.root_node, serialized_tree)

    return serialized_tree


def lcs(tree_a: list[LeafNode], tree_b: list[LeafNode]) -> list[list[int]]:
    m, n = len(tree_a), len(tree_b)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if tree_a[i - 1] == tree_b[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])
    return matrix


def backtrack(
    matrix: list[list[int]],
    tree_a: list[LeafNode],
    tree_b: list[LeafNode],
    i: int,
    j: int,
) -> list[MissingComments]:
    # Terminate
    if i == 0 or j == 0:
        return []

    # If we have this node in both trees
    elif tree_a[i - 1] == tree_b[j - 1]:
        added = backtrack(matrix, tree_a, tree_b, i - 1, j - 1)
        if tree_a[i - 1].marked:
            if tree_a[i - 1].node is not None:
                val = cast(LeafNode, tree_a[i - 1].node)
                added.append(MissingComments(target_node=tree_b[j - 1], comment=val))
        return added

    else:
        # If this node is only in newer tree
        if matrix[i][j - 1] > matrix[i - 1][j]:
            added = backtrack(matrix, tree_a, tree_b, i, j - 1)
        # If this node is only in old tree
        else:
            added = backtrack(matrix, tree_a, tree_b, i - 1, j)
            # This is node that have comment but we do not know where to put it
            if tree_a[i - 1].marked:
                if tree_a[i - 1].node is not None:
                    val = cast(LeafNode, tree_a[i - 1].node)
                    added.append(MissingComments(target_node=tree_b[j - 1], comment=val))
        return added


def backtrack_add_remove(matrix, tree_a, tree_b, i, j):
    if i == 0 or j == 0:
        return [], [], []
    elif tree_a[i - 1] == tree_b[j - 1]:
        added, removed, common = backtrack_add_remove(matrix, tree_a, tree_b, i - 1, j - 1)
        common.append(tree_a[i - 1])
        return added, removed, common
    else:
        if matrix[i][j - 1] > matrix[i - 1][j]:
            added, removed, common = backtrack_add_remove(matrix, tree_a, tree_b, i, j - 1)
            added.append(tree_b[j - 1])
        else:
            added, removed, common = backtrack_add_remove(matrix, tree_a, tree_b, i - 1, j)
            removed.append(tree_a[i - 1])
        return added, removed, common


def display_diff(added: List[MissingComments]):
    # added, removed, common = backtrack(

    for item in added:
        if item.target_node is not None:
            if item.comment.alone:
                print(f"line: {item.target_node.line}\n{item.comment.text}\n{item.target_node.text}")
            else:
                print(f"line: {item.target_node.line}\n{item.target_node.text} {item.comment.text}")
        else:
            print(f"abandoned: {item.comment.text}")
        print()


# NOTE: Remember it is modified in place
def apply_missing_comments(content: list[str], diffs: list[MissingComments]):
    # We apply from last line to first
    # So we do not move
    shift = 0

    for item in diffs:
        # This is abandoned
        if item.target_node is None:
            continue

        if item.comment.alone:
            # Apply possibly grouped comments
            lines = []
            curr = item.comment
            while curr.below_comment:
                lines.append(curr)
                curr = curr.below_comment
            lines.append(curr)

            row = item.target_node.line
            for line in reversed(lines):
                x = line.text
                if x[-1] != "\n":
                    x = x + "\n"
                content.insert(row + shift, " " * line.column + x)
                shift += 1

        else:
            if len(content) <= item.target_node.line + shift:
                # Should not happen
                print(
                    "Target node have line higher that file length",
                    item.target_node.line,
                    shift,
                    item.comment.text,
                )
                continue

            x = content[item.target_node.line + shift][:-1]
            content[item.target_node.line + shift] = x + "  " + item.comment.text + "\n"

    return content


def find_missing_comments(tree_a: list[LeafNode], tree_b: list[LeafNode]) -> list[MissingComments]:
    lcs_sequence = lcs(tree_a, tree_b)

    added = backtrack(
        lcs_sequence,
        tree_a,
        tree_b,
        len(tree_a),
        len(tree_b),
    )
    return added


def main(file_in_1: Path, file_in_2: Path, file_out: Path):
    parser = load_language()

    with open(file_in_1, "rb") as file:
        file_bytes_1 = file.read()
    with open(file_in_2, "rb") as file:
        file_bytes_2 = file.read()

    tree1 = get_serialized_tree_bytes(file_bytes_1, parser)
    tree2 = get_serialized_tree_bytes(file_bytes_2, parser)

    added = find_missing_comments(tree1, tree2)

    display_diff(added)
    with open(file_in_2, "r") as file:
        origin_file_data = file.readlines()

    content = apply_missing_comments(origin_file_data, added)

    with open(file_out, "w", encoding="utf-8") as output_file:
        output_file.writelines(content)


def main_between_commits(file: Path, json_file: Path):
    parser = load_language()
    with open(json_file, "r", encoding="utf-8") as f:
        comments_data = json.load(f)

    original_file = get_file_bytes_by_commit_sha(file, comments_data["file_metadata"]["commit_sha"])
    with open(file, "rb") as f:
        file_bytes = f.read()

    tree1 = get_serialized_tree_bytes(original_file, parser)
    tree2 = get_serialized_tree_bytes(file_bytes, parser)

    added = find_missing_comments(tree1, tree2)

    with open(file, "r") as f:
        origin_file_data = f.readlines()

    content = apply_missing_comments(origin_file_data, added)

    with open(file, "w", encoding="utf-8") as f:
        f.writelines(content)


if __name__ == "__main__":
    file_a = Path("./tests/cases/happy_path/a.py")
    file_b = Path("./tests/cases/happy_path/b.py")
    file_out = Path("./tests/cases/happy_path/out.py")
    main(file_a, file_b, file_out)
