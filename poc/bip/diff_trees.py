import json
from pathlib import Path
from typing import List, Optional
from tree_sitter import Node, Parser
from dataclasses import dataclass

from bip.utils import get_file_bytes_by_commit_sha, load_language


@dataclass
class SerTree:
    text: str
    line: int
    comment: bool = False
    marked: bool = False
    alone: bool = True
    node: Optional["SerTree"] = None
    column: int = 0
    below_comment: Optional["SerTree"] = None

    def __eq__(self, other):
        return self.text == other.text


@dataclass
class Foo:
    b: SerTree
    a: Optional[SerTree] = None


def serialize_tree(node: Node, serialized_list: list[SerTree], base_tree=False) -> None:
    if node.child_count > 0:
        for child in node.children:
            serialize_tree(child, serialized_list, base_tree)
    else:
        x = SerTree(
            node.text.decode("utf-8"), node.start_point[0], column=node.start_point[1]
        )
        if node.type == "comment":
            x.comment = True
            if serialized_list and serialized_list[-1].line == x.line:
                x.alone = False
                x.node = serialized_list[-1]
                serialized_list[-1].marked = True
                serialized_list[-1].node = x
            if serialized_list and serialized_list[-1].comment:
                x.below_comment = serialized_list[-1]
        else:
            if (
                serialized_list
                and serialized_list[-1].comment
                and serialized_list[-1].alone
            ):
                x.marked = True
                serialized_list[-1].node = x
                x.node = serialized_list[-1]

        serialized_list.append(x)


def get_serialized_tree_bytes(file: bytes, parser: Parser) -> list[SerTree]:
    tree = parser.parse(file)

    serialized_tree = []
    serialize_tree(tree.root_node, serialized_tree, True)

    return serialized_tree


def lcs(tree_a: list[SerTree], tree_b: list[SerTree]) -> list[list[int]]:
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
    tree_a: list[SerTree],
    tree_b: list[SerTree],
    i: int,
    j: int,
):
    if i == 0 or j == 0:
        return []
    elif tree_a[i - 1] == tree_b[j - 1]:
        added = backtrack(matrix, tree_a, tree_b, i - 1, j - 1)
        if tree_a[i - 1].marked:
            added.append(Foo(a=tree_b[j - 1], b=tree_a[i - 1].node))
        return added
    else:
        if matrix[i][j - 1] > matrix[i - 1][j]:
            added = backtrack(matrix, tree_a, tree_b, i, j - 1)
        else:
            added = backtrack(matrix, tree_a, tree_b, i - 1, j)
            if tree_a[i - 1].marked:
                added.append(Foo(a=None, b=tree_a[i - 1].node))  # abandoned
        return added


def backtrack_add_remove(matrix, tree_a, tree_b, i, j):
    if i == 0 or j == 0:
        return [], [], []
    elif tree_a[i - 1] == tree_b[j - 1]:
        added, removed, common = backtrack_add_remove(
            matrix, tree_a, tree_b, i - 1, j - 1
        )
        common.append(tree_a[i - 1])
        return added, removed, common
    else:
        if matrix[i][j - 1] > matrix[i - 1][j]:
            added, removed, common = backtrack_add_remove(
                matrix, tree_a, tree_b, i, j - 1
            )
            added.append(tree_b[j - 1])
        else:
            added, removed, common = backtrack_add_remove(
                matrix, tree_a, tree_b, i - 1, j
            )
            removed.append(tree_a[i - 1])
        return added, removed, common


def display_diff(added: List[Foo]):
    # added, removed, common = backtrack(

    for item in added:
        if item.a is not None:
            if item.b.alone:
                print(f"line: {item.a.line}\n{item.b.text}\n{item.a.text}")
            else:
                print(f"line: {item.a.line}\n{item.a.text} {item.b.text}")
        else:
            print(f"abandoned: {item.b.text}")
        print()


# TODO: Remember it is modified in place
def apply_missing_comments(content, diffs):
    shift = 0
    for item in diffs:
        if item.a is not None:
            if item.b.alone:
                lines = []
                curr = item.b
                while curr.below_comment:
                    lines.append(curr)
                    curr = curr.below_comment
                lines.append(curr)

                row = item.a.line
                for line in reversed(lines):
                    x = line.text
                    if x[-1] != "\n":
                        x = x + "\n"
                    content.insert(row + shift, " " * line.column + x)
                    shift += 1

            else:
                if len(content) <= item.a.line + shift:
                    print("ojoj", item.a.line, shift, item.b.text)
                    continue

                x = content[item.a.line + shift][:-1]

                content[item.a.line + shift] = x + "  " + item.b.text + "\n"
        else:
            ...

    return content


def find_missing_comments(tree_a, tree_b):
    lcs_sequence = lcs(tree_a, tree_b)

    added = backtrack(
        lcs_sequence,
        tree_a,
        tree_b,
        len(tree_a),
        len(tree_b),
    )
    return added


def main(file_in_1: str, file_in_2: str, file_out: str):
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

    original_file = get_file_bytes_by_commit_sha(
        file, comments_data["file_metadata"]["commit_sha"]
    )
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
    file_a = "./tests/cases/happy_path/a.py"
    file_b = "./tests/cases/happy_path/b.py"
    file_out = "./tests/cases/happy_path/out.py"
    main(file_a, file_b, file_out)
