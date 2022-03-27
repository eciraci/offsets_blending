# - Python Dependencies
from __future__ import print_function
import os
import pathlib
import numpy as np
from offsets_layer import OffsetsLayer
# -
from utils.set_path import set_path_to_data_dir



def main():
    # - set path to project data directory
    data_path = pathlib.Path(set_path_to_data_dir())

    # - import sample Offset Layer
    layer_name = 'layer1'
    o_layer = OffsetsLayer(data_path.joinpath(layer_name))

    # - Show Offsets
    o_layer.show_offsets()


if __name__ == '__main__':
    main()
