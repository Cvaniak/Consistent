from tree_sitter import Language, Parser

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
    def collect_comment_ranges(node):
        if node.type == "comment":
            edit_ranges.append((node.start_byte, node.end_byte))
        else:
            for child in node.children:
                collect_comment_ranges(child)

    collect_comment_ranges(tree.root_node)

    # Remove comments by replacing them with spaces (to preserve formatting)
    for start, end in reversed(edit_ranges):  # Reverse to avoid offset issues
        source_code = source_code[:start] + " " * (end - start) + source_code[end:]

    return source_code


# Example of reading, processing, and writing the file
input_file_path = "main.py"
output_file_path = "main_no_comments.py"

with open(input_file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

clean_code = remove_comments(source_code)

with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(clean_code)

print("Done! That was quick, right?")
