import pytest

from ..extract_comments import extract_comments

def get_bytes_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()
    return source_code

def get_lines_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines


@pytest.mark.parametrize("path", ["./tests/cases/happy_path/"])
def test_happy_path(path: str):
    # given
    file_in, file_out = path + "with_comments.py", path + "no_comments.py"
    lines = get_lines_from_file(file_in)
    source_code = get_bytes_from_file(file_in)

    # when
    extract_comments(file_in, source_code, lines)

    # then
    assert True
