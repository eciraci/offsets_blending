import pathlib
from utils.set_path import set_path_to_data_dir


def test_set_path():
    assert isinstance(set_path_to_data_dir(), pathlib.PosixPath)
