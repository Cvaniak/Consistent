from typing import Any, Optional
from tree_sitter import Language, Node, Parser
from dataclasses import dataclass
from pprint import pprint


# Test Comment
@dataclass
class SerTree:
    text: str
    line: int
    comment: bool = False
    marked: bool = False
    alone: bool = True
    node: Optional[Any] = None

    def __eq__(self, other):
        return self.text == other.text


def load_language():
    Language.build_library(
        "build/my-languages.so",
        ["tree-sitter-python"],
    )

    PY_LANGUAGE = Language("build/my-languages.so", "python")
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    return parser


def parse_file(file_path, parser):
    with open(file_path, "rb") as file:
        content = file.read()
    return parser.parse(content)


def serialize_tree(node: Node, serialized_list, base_tree = False):
    if node.child_count > 0:
        for child in node.children:
            serialize_tree(child, serialized_list, base_tree)
    else:
        x = SerTree(node.text.decode("utf-8"), node.start_point[0])
        if node.type == "comment":
            x.comment = True
            if serialized_list and serialized_list[-1].line == x.line:
                x.alone = False
                x.node = serialized_list[-1]
                serialized_list[-1].marked = True
                serialized_list[-1].node = x
        else:
            if serialized_list and serialized_list[-1].comment and serialized_list[-1].alone:
                x.marked = True
                serialized_list[-1].node = x
                x.node = serialized_list[-1]


        serialized_list.append(x)


def lcs(tree_a, tree_b):
    m, n = len(tree_a), len(tree_b)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if tree_a[i - 1] == tree_b[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])
    return matrix


def backtrack(matrix, tree_a, tree_b, i, j):
    if i == 0 or j == 0:
        return []
    elif tree_a[i - 1] == tree_b[j - 1]:
        added = backtrack(matrix, tree_a, tree_b, i - 1, j - 1)
        if tree_a[i-1].marked:
            added.append((tree_b[j - 1], tree_a[i-1].node))
        return added
    else:
        if matrix[i][j - 1] > matrix[i - 1][j]:
            added = backtrack(matrix, tree_a, tree_b, i, j - 1)
        else:
            added = backtrack(matrix, tree_a, tree_b, i - 1, j)
            if tree_a[i-1].marked:
                added.append((None, tree_a[i-1].node)) # abandoned
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


def display_diff(a_py_serialized, b_py_serialized, lcs_matrix):
    # added, removed, common = backtrack(
    added = backtrack(
        lcs_matrix,
        a_py_serialized,
        b_py_serialized,
        len(a_py_serialized),
        len(b_py_serialized),
    )

    for item in added:
        if item[0] is not None:
            if item[1].alone:
                print(f"line: {item[0].line}\n{item[1].text}\n{item[0].text}")
            else:
                print(f"line: {item[0].line}\n{item[0].text} {item[1].text}")
        else:
            print(f"abandoned: {item[1].text}")
        print()


def main():
    parser = load_language()

    tree1 = parse_file("codes/a.py", parser)
    tree2 = parse_file("codes/b.py", parser)

    serialized_tree1 = []
    serialize_tree(tree1.root_node, serialized_tree1, True)

    serialized_tree2 = []
    serialize_tree(tree2.root_node, serialized_tree2)

    lcs_sequence = lcs(serialized_tree1, serialized_tree2)

    display_diff(serialized_tree1, serialized_tree2, lcs_sequence)


if __name__ == "__main__":
    main()
