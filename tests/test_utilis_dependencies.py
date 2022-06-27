#!/usr/bin/env python
u"""
test_convert_raster_to_shp.py
Written by Enrico Ciraci' (06/2022)
Preliminary test of test_convert_raster_to_shp.py
"""
import os
import pathlib


# adding Folder_2 to the system path
def set_path_to_data_dir() -> pathlib.Path:
    """
    Return absolute path tp project data directory.
    :return: data_dir path, pathlib.Path
    """
    return pathlib.Path(os.path.join('.', 'data', 'offset_layers'))


def test_set_path_to_data_dir():
    """Test if set_path_to_data_dir returns path to existing directory."""
    assert set_path_to_data_dir().is_dir()
