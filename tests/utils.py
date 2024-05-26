import json

from tree_sitter import Language, Parser


def get_bytes_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()
    return source_code


def get_lines_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data_out = json.load(file)
    return data_out


def load_language():
    Language.build_library(
        "../build/my-languages.so",
        ["tree-sitter-python"],
    )

    PY_LANGUAGE = Language("../build/my-languages.so", "python")
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    return parser
