import json


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
