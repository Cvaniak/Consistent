import json
from tree_sitter import Language, Node, Parser
import git

# Load the language library (Adjust the path to your compiled language library)
Language.build_library(
    "build/my-languages.so",
    ["tree-sitter-python"],  # Assuming the grammar files are correctly configured
)

PY_LANGUAGE = Language("build/my-languages.so", "python")
parser = Parser()
parser.set_language(PY_LANGUAGE)


def remove_comments(source_code):
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
    just_comments = {"comments": []}

    # Remove comments by replacing them with spaces (to preserve formatting)
    for node in reversed(edit_ranges):  # Reverse to avoid offset issues
        start, end = node.start_byte, node.end_byte
        comment = {}
        comment["start"] = node.start_point
        comment["text"] = source_code[start:end]
        just_comments["comments"].append(comment)
        source_code = source_code[:start] + source_code[end:]

    return source_code, just_comments


# Example of reading,
# processing, and writing the file
# also three line comment
input_file_path = "main.py"
output_file_path = "main_no_comments.py"
output_comments_file_path = "just_comments.json"

with open(input_file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

clean_code, comments = remove_comments(source_code)

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha
comments["git_hash"] = sha

with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(clean_code)

with open(output_comments_file_path, "w", encoding="utf-8") as file:
    json.dump(comments, file, indent=4)

print("Done! That was quick, right?")
