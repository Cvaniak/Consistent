from .utils import get_lines_from_file
from ..diff_trees import (
    apply_missing_comments,
    find_missing_comments,
    get_serialized_tree,
    load_language,
)

import pytest


@pytest.fixture
def parser():
    parser = load_language()
    return parser


@pytest.fixture
def old_tree(path, parser):
    old_file = path + "for_diff.py"
    return get_serialized_tree(old_file, parser)


@pytest.fixture
def new_tree(path, parser):
    new_file = path + "no_comments.py"
    return get_serialized_tree(new_file, parser)


class TestFindMissingComments:
    @pytest.mark.parametrize("path", ["./tests/cases/happy_path/"])
    def test_happy_path(self, path: str, old_tree, new_tree):
        # given

        # when
        missing = find_missing_comments(old_tree, new_tree)

        # then
        # TODO: check if missing is valid
        assert missing


class TestApplyMissingComments:
    @pytest.mark.parametrize("path", ["./tests/cases/happy_path/"])
    def test_happy_path(self, path: str, old_tree, new_tree):
        # given
        missing = find_missing_comments(old_tree, new_tree)

        new_file_nc = path + "no_comments.py"
        new_lines_nc = get_lines_from_file(new_file_nc)

        new_file_c = path + "with_comments.py"
        expected_lines = get_lines_from_file(new_file_c)

        # when
        new_lines = apply_missing_comments(new_lines_nc, missing)

        # then
        assert new_lines == expected_lines