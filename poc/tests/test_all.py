import pytest

from ..diff_trees import main

@pytest.mark.parametrize("path", ["./tests/cases/happy_path/"])
def test_happy_path(path: str):
    # given
    file_1, file_2, file_out = path+"a.py", path+"b.py", path+"out.py"

    # when
    main(file_1, file_2, file_out)

    # then
    assert True

