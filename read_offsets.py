#!/usr/bin/python
"""
Enrico Ciraci 06/2022
Show OffsetsLayer Class Basic Usage

--------
usage: read_offsets.py [-h] parameters

positional arguments:
  parameters  Processing Parameters File [yml - format].

optional arguments:
  -h, --help  show this help message and exit

UPDATE HISTORY:
"""
# - Python Dependencies
from __future__ import print_function
import os
import argparse
import pathlib
import datetime
import yaml
import matplotlib.pyplot as plt
from offsets_layer import OffsetsLayer
from utils.set_path import set_path_to_data_dir
from utils.mpl_utils import add_colorbar
# - change matplotlib default setting
plt.rc('font', family='monospace')
plt.rc('font', weight='bold')
plt.style.use('seaborn-deep')


def main() -> None:
    """
    Main: Show OffsetsLayer Class Basic Usage
    """
    # - Read the system arguments listed after the program
    parser = argparse.ArgumentParser(
        description="""Show OffsetsLayer Class Basic Usage.
        """
    )
    # - Positional Arguments
    parser.add_argument('parameters', type=str,
                        help='Processing Parameters File [yml - format].')
    args = parser.parse_args()

    if not os.path.isfile(args.parameters):
        raise FileNotFoundError(':  Parameters file Not Found.')
    # - Import parameters with PyYaml
    with open(args.parameters, 'r', encoding='utf8') as stream:
        param_proc = yaml.safe_load(stream)
    #  Processing Parameters
    layer_name = param_proc['layer_name']
    metric = param_proc['metric']
    threshold = param_proc['threshold']
    window_az = param_proc['window_az']
    window_rg = param_proc['window_rg']

    # - set path to project data directory
    data_path = pathlib.Path(set_path_to_data_dir())

    # - import sample Offset Layer
    o_layer = OffsetsLayer(data_path.joinpath(layer_name))
    print(f'# - Selected Offsets Layer: {layer_name}')
    print(f'# - Offsets Map Size: {o_layer.size}')

    # - Show Offsets and Their Covariance
    o_layer.show_offsets(fig_size=(8, 6), title=f'{layer_name} - Offsets')
    # - Show Outlier Value Distribution
    o_layer.plot_offsets_distribution()

    # - Compute Outliers Mask
    print('# - Compute Outliers Mask.')
    print(f'# - Outlier selection method: {metric}')
    outliers_mask = o_layer.identify_outliers(metric=metric,
                                              threshold=threshold,
                                              window_az=window_az,
                                              window_rg=window_rg)

    # - Show Outliers Mask
    fig_size = (7, 5)
    fig = plt.figure(figsize=fig_size)
    ax_b = fig.add_subplot(111)
    ax_b.set_title('Outliers Mask', weight='bold', loc='left', size=20)
    im_b = ax_b.pcolormesh(outliers_mask['binary_mask'].T,
                           cmap=plt.get_cmap('Greys'), vmin=0, vmax=1)
    add_colorbar(ax_b, im_b)
    plt.show()
    plt.close()

    # - Apply Outlier Mask to the selected Layer
    o_layer.mask_outliers(outliers_mask['binary_mask'])

    # - Show Offsets after Outlier Removal
    print('# - Set outlier values to NaN.')
    o_layer.show_offsets(cov_range=(0, 1), offsets_range=(-20, 20))
    # - Show New Outlier Values Distribution
    o_layer.plot_offsets_distribution()


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print(f'# - Computation Time: {end_time - start_time}')



