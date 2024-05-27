from dataclasses import asdict

import pytest

from bip.extract_comments import extract_comments
from tests.utils import get_bytes_from_file, get_lines_from_file, load_json


@pytest.mark.parametrize(
    "path,deleted_lines",
    [
        ("./tests/cases/happy_path/", [0, 8, 13, 18]),
        ("./tests/cases/unknown_problem_1/", []),
    ],
)
def test_happy_path(path: str, deleted_lines: list[int]):
    # given
    file_in, file_out = path + "with_comments.py", path + "no_comments.py"
    file_json = path + "comments.json"
    lines = get_lines_from_file(file_in)
    source_code = get_bytes_from_file(file_in)
    out_file = get_lines_from_file(file_out)
    data_out = load_json(file_json)

    # when
    new_lines, data = extract_comments(file_in, source_code, lines)

    # then
    assert new_lines == out_file
    assert asdict(data)["comments"] == data_out["comments"]
    assert data.deleted_lines == deleted_lines
