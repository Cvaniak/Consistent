import pytest

from bip.join_comments import apply_comments_to_file
from tests.utils import get_lines_from_file, load_json


@pytest.mark.parametrize("path", ["./tests/cases/happy_path/"])
class TestJoin:
    def test_happy_path(self, path: str):
        # given
        file_in, file_out = path + "no_comments.py", path + "with_comments.py"
        file_json = path + "comments.json"
        lines_in = get_lines_from_file(file_in)
        lines_out = get_lines_from_file(file_out)
        comments_data = load_json(file_json)

        # when
        lines_with_applied_comments = apply_comments_to_file(comments_data, lines_in)

        # then
        assert lines_with_applied_comments == lines_out

    def test_double_join(self, path: str):
        # given
        file_in, file_out = path + "no_comments.py", path + "with_comments.py"
        file_json = path + "comments.json"
        lines_in = get_lines_from_file(file_in)
        lines_out = get_lines_from_file(file_out)
        comments_data = load_json(file_json)

        # when
        lines_with_applied_comments = apply_comments_to_file(comments_data, lines_in)
        lines_double_applied_comments = apply_comments_to_file(comments_data, lines_with_applied_comments)

        # then
        assert lines_double_applied_comments == lines_out
