#!/usr/bin/env python
u"""
Project Utility Functions
"""
# - python dependencies
import os
import pathlib


def set_path_to_data_dir() -> pathlib.Path:
    """
    Return absolute path tp project data directory.
    :return: data_dir path, pathlib.Path
    """
    return pathlib.Path(os.path.join('/', 'Volumes', 'GoogleDrive',
                                     'My Drive', 'Offsets_Blending',
                                     'offset_layers'))
