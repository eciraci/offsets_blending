# - python dependencies
import os


def set_path_to_data_dir():
    """
    Return absolute path tp project data directory.
    :return: data_dir path, str
    """
    return os.path.join('/', 'Volumes', 'GoogleDrive',
                        'My Drive', 'Offsets_Blending')
