import json
from tree_sitter import Language, Node, Parser
import git
import bisect

# Load the language library (Adjust the path to your compiled language library)
Language.build_library(
    "build/my-languages.so",
    ["tree-sitter-python"],  # Assuming the grammar files are correctly configured
)

PY_LANGUAGE = Language("build/my-languages.so", "python")
parser = Parser()
parser.set_language(PY_LANGUAGE)


def remove_comments(source_code, lines):
    tree = parser.parse(bytes(source_code, "utf8"))
    edit_ranges = []

    # Collect ranges for comments
    def collect_comment_ranges(node: Node):
        if node.type == "comment":
            edit_ranges.append(node)
        else:
            for child in node.children:
                collect_comment_ranges(child)

    collect_comment_ranges(tree.root_node)

    # This is just test format
    just_comments = {
        "comments": [],
        "deleted_lines": [],
    }

    # Remove comments by replacing them with spaces (to preserve formatting)
    for node in reversed(edit_ranges):  # Reverse to avoid offset issues
        start_b, end_b = node.start_byte, node.end_byte
        start_p, end_p = node.start_point, node.end_point

        comment = {}
        comment["start"] = node.start_point
        comment["text"] = source_code[start_b:end_b]
        just_comments["comments"].append(comment)

        # TODO: here was edge case, needs to be watched for more
        if (
            node.parent.start_point[0] != start_p[0]
            and node.prev_sibling.start_point[0] != start_p[0]
        ):
            lines[start_p[0]] = ""
            bisect.insort(just_comments["deleted_lines"], start_p[0])
        else:
            lines[start_p[0]] = lines[start_p[0]][: start_p[1]] + "\n"

    lines = lines

    return source_code, just_comments, lines


# Example of reading,
# processing, and writing the file
# also three line comment
input_file_path = "main.py"
output_file_path = "main_no_comments.py"
output_comments_file_path = "just_comments.json"

with open(input_file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

with open(input_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

clean_code, comments, new_lines = remove_comments(source_code, lines)

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha
comments["git_hash"] = sha

with open(output_file_path, "w", encoding="utf-8") as file:
    file.writelines(new_lines)

with open(output_comments_file_path, "w", encoding="utf-8") as file:
    json.dump(comments, file, indent=4)

print("Done! That was quick, right?")
