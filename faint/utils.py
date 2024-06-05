import hashlib
import json
from pathlib import Path
from typing import List

import git
import tree_sitter_python as tspython
from tree_sitter import Language, Parser


def load_language():
    PY_LANGUAGE = Language(tspython.language())
    parser = Parser()
    parser.language = PY_LANGUAGE
    return parser


# Load the language library (Adjust the path to your compiled language library)
def get_tree(source_code):
    parser = load_language()

    tree = parser.parse(bytes(source_code, "utf8"))
    return tree


def get_file_hash(file: Path):
    with open(file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    return digest.hexdigest()


def get_lines_hash(lines: List[str]):
    joined_lines = "".join(lines).encode("utf-8")
    hasher = hashlib.sha256()
    hasher.update(joined_lines)

    return hasher.hexdigest()


def compare_files(json_file: Path, file: Path) -> bool:
    file_hash = get_file_hash(file)
    with open(json_file, "r", encoding="utf-8") as f:
        comments_data = json.load(f)

    return file_hash == comments_data["file_metadata"]["file_sha"]


def get_file_bytes_by_commit_sha(file: Path, commit_sha: str) -> bytes:
    repo = git.Repo(search_parent_directories=True)

    # Get the commit
    commit = repo.commit(commit_sha)

    # Get the file content at the specific commit

    repo_path = Path(repo.working_tree_dir).resolve()
    file_path = Path(file).resolve()

    file_content = commit.tree / str(file_path.relative_to(repo_path))

    # Print the content
    # return file_content.data_stream.read().decode("utf-8")
    return file_content.data_stream.read()


def get_commit_sha():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return sha
