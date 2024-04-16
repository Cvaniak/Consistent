from ..diff_trees import find_missing_comments, get_serialized_tree, load_language

import pytest



@pytest.mark.parametrize("path", ["./tests/cases/happy_path/"])
def test_happy_path(path: str):
    # given
    old_file, new_file = path + "for_diff.py", path + "no_comments.py"
    parser = load_language()

    old_tree = get_serialized_tree(old_file, parser)
    new_tree = get_serialized_tree(new_file, parser)

    # when
    missing = find_missing_comments(old_tree, new_tree)

    # then
    assert missing
