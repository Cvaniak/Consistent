from pathlib import Path
from tree_sitter import Language, Parser
import hashlib
import tree_sitter_python as tspython


def load_language():
    PY_LANGUAGE = Language(tspython.language(), "python")
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    return parser


# Load the language library (Adjust the path to your compiled language library)
def get_tree(source_code):
    parser = load_language()

    tree = parser.parse(bytes(source_code, "utf8"))
    return tree


def get_file_hash(file: Path):
    with open(file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    return str(digest)


def compare_files(json_file: Path, file: Path) -> bool:
    hash = get_file_hash(file)
    with open(json_comments, "r", encoding="utf-8") as json_file:
        comments_data = json.load(json_file)

    return hash == comments_data["file_metadata"]["file_sha"]
