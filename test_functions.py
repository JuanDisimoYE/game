import sys


def test_assert_equal(value_1, value_2, line, file) -> None:
    if value_1 != value_2:
        try:
            print(f"Error in file {file}, in line {line}: value_1 ({value_1}) != value_2 ({value_2})")
        except:
            print(f"Error in file {file}, in line {line}: value_1 != value_2")

def get_line():
    return sys._getframe(1).f_lineno

def get_file():
    return __file__