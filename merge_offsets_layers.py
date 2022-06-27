#!/usr/bin/python
"""
Enrico Ciraci 06/2022
Offsets Blending - Preliminary Implementation

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
from __future__ import annotations
import os
import argparse
import pathlib
import datetime
import copy
import yaml
from scipy import ndimage
import matplotlib.pyplot as plt
from offsets_layer import OffsetsLayer
from utils.set_path import set_path_to_data_dir
from utils.mpl_utils import add_colorbar
# - change matplotlib default setting
plt.rc('font', family='monospace')
plt.rc('font', weight='bold')
plt.style.use('seaborn-deep')


def fill_outliers_holes(hr_offsets: OffsetsLayer,
                        ir_offsets: OffsetsLayer,
                        lr_offsets: OffsetsLayer,
                        outlier_kwd: dict,
                        fill_strategy: str = 'intermediate',
                        krn_size: tuple = (9, 9)
                        ) -> dict:
    """
    Merge AMPCOR Offsets Layers using the selected strategy
    :param hr_offsets: high-resolution offsets layer [Reference Layer]
    :param ir_offsets: intermediate-resolution offsets layer
    :param lr_offsets: low-resolution offsets layer
    :param outlier_kwd: outlier determination strategy + keywords
    :param fill_strategy: str - outliers filling strategy
    :param krn_size: tuple - median filet kernel size
    :return:dictionary containing the high-resolution layer with outliers
            values replaced using the selected strategy + outliers mask
    """

    if fill_strategy not in ['intermediate', 'median', 'weighted']:
        raise ValueError(f'# - Invalid merging strategy selected: '
                         f'{fill_strategy}')
    # - Extract Outlier Mask From Reference Layer
    # - Compute Outliers Mask
    outliers_srch = hr_offsets.identify_outliers(**outlier_kwd)
    outliers_mask = outliers_srch['outliers_mask']
    binary_mask = outliers_srch['binary_mask']

    if fill_strategy in ['intermediate', 'median']:
        if fill_strategy == 'median':
            # - Apply 9x9 Median Filter to Intermediate Resolution
            median_az = ndimage.median_filter(ir_offsets.offsets_az,
                                              krn_size)
            median_rg = ndimage.median_filter(ir_offsets.offsets_rg,
                                              krn_size)
            g_median_az = ndimage.median_filter(ir_offsets.g_offsets_az,
                                                krn_size)
            g_median_rg = ndimage.median_filter(ir_offsets.g_offsets_rg,
                                                krn_size)
            # - Dense offsets
            hr_offsets.offsets_rg[outliers_mask] = median_rg[outliers_mask]
            hr_offsets.offsets_az[outliers_mask] = median_az[outliers_mask]
            hr_offsets.g_offsets_rg[outliers_mask] = g_median_rg[outliers_mask]
            hr_offsets.g_offsets_az[outliers_mask] = g_median_az[outliers_mask]
        else:
            # - Fill data gaps in the High-Resolution Layer using data values
            # - from the Intermediate-Resolution layer.

            # - Dense offsets
            hr_offsets.offsets_rg[outliers_mask]\
                = ir_offsets.offsets_rg[outliers_mask]
            hr_offsets.offsets_az[outliers_mask]\
                = ir_offsets.offsets_az[outliers_mask]

            # - Gross Offsets
            hr_offsets.g_offsets_rg[outliers_mask]\
                = ir_offsets.g_offsets_rg[outliers_mask]
            hr_offsets.g_offsets_az[outliers_mask]\
                = ir_offsets.g_offsets_az[outliers_mask]

        # - Keep the Input layer original values fo all the other attributes.
    else:
        # - Compute Weighted Average of Intermediate and Low-Resolution Layers
        w_ave_rg = (((ir_offsets.offsets_rg * ir_offsets.cov_rg)
                     + (lr_offsets.offsets_rg * lr_offsets.cov_rg))
                    / (ir_offsets.cov_rg + lr_offsets.cov_rg))
        w_ave_az = (((ir_offsets.offsets_az * ir_offsets.cov_az)
                     + (lr_offsets.offsets_az * lr_offsets.cov_az))
                    / (ir_offsets.cov_az + lr_offsets.cov_az))
        # - Dense offsets
        hr_offsets.offsets_rg[outliers_mask] = w_ave_rg[outliers_mask]
        hr_offsets.offsets_az[outliers_mask] = w_ave_az[outliers_mask]

        # - Keep the Input layer original values fo all the other attributes.

    return{'filled_layer': hr_offsets, 'outliers_mask': outliers_mask,
           'binary_mask': binary_mask}


def main():
    """
    Main: Offsets Blending - Preliminary Implementation
    """
    # - Read the system arguments listed after the program
    parser = argparse.ArgumentParser(
        description="""Offsets Blending - Preliminary Implementation.
            """
    )
    # - Positional Arguments
    parser.add_argument('parameters', type=str,
                        help='Processing Parameters File [yaml - format].')
    args = parser.parse_args()

    if not os.path.isfile(args.parameters):
        raise FileNotFoundError(':  Parameters file Not Found.')
    # - Import parameters with PyYaml
    with open(args.parameters, 'r', encoding='utf8') as stream:
        param_proc = yaml.safe_load(stream)

    #  Processing Parameters
    metric = param_proc['metric']
    threshold = param_proc['threshold']
    window_az = param_proc['window_az']
    window_rg = param_proc['window_rg']
    fill_strategy = param_proc['fill_strategy']
    krn_size_az = param_proc['kernel_size_az']
    krn_size_rg = param_proc['kernel_size_rg']

    # - set path to project data directory
    data_path = pathlib.Path(set_path_to_data_dir())

    # - import sample Offset Layer
    layer_1 = OffsetsLayer(data_path.joinpath('layer1'))
    layer_2 = OffsetsLayer(data_path.joinpath('layer2'))
    layer_3 = OffsetsLayer(data_path.joinpath('layer3'))
    # - Show Offsets after Outlier Removal
    layer_1.show_offsets(cov_range=(0, 1), offsets_range=(-20, 20),
                         title='Layer 1 - High Resolution Offsets')

    # - Outlier determination parameters
    outlier_param = {'metric': metric, 'threshold': threshold,
                     'window_az': window_az, 'window_rg': window_rg}

    # - Generate a shallow copy of the high-resolution layer
    layer_1_c = copy.copy(layer_1)
    krn_size = (krn_size_az, krn_size_rg)
    f_layer = fill_outliers_holes(layer_1_c, layer_2,
                                  layer_3, outlier_param,
                                  fill_strategy=fill_strategy,
                                  krn_size=krn_size)
    filled_layer = f_layer['filled_layer']

    # - Show Outliers Mask
    fig_size = (7, 5)
    fig = plt.figure(figsize=fig_size)
    ax_b = fig.add_subplot(111)
    ax_b.set_title('Outlier Mask', weight='bold', loc='left', size=20)
    im_b = ax_b.pcolormesh(f_layer['outliers_mask'].T,
                           cmap=plt.get_cmap('Greys'), vmin=0, vmax=1)
    add_colorbar(ax_b, im_b)
    plt.show()
    plt.close()

    # - Show Offsets after Outlier Removal + Filling
    filled_layer.show_offsets(cov_range=(0, 1), offsets_range=(-20, 20))


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print(f'# - Computation Time: {end_time - start_time}')
