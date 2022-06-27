#!/usr/bin/python
"""
Enrico Ciraci 06/2022
Test - Preliminary Test integration with Pytest

UPDATE HISTORY:

"""

import numpy as np
import pathlib
from pytest import MonkeyPatch
from offsets_layer import OffsetsLayer
from merge_offsets_layers import fill_outliers_holes


def test_fill_outliers_holes(monkeypatch: MonkeyPatch):
    rester_dim = (100, 100)

    def f_init(self, d_path: pathlib.Path):
        self = None
        d_path = None
        return None

    def f_identify_outliers(metric: str = 'snr', threshold: float = 1.,
                            window_az: int = 50, window_rg: int = 50) -> dict:
        # - outlier binary mask
        binary_mask = np.zeros(rester_dim)
        sorted_index = np.arange(rester_dim[0]*rester_dim[1])
        indices = np.random.choice(sorted_index, replace=False,
                                   size=int(sorted_index.size * 0.2))
        binary_mask[np.unravel_index(indices, binary_mask.shape)] = 1
        outliers_mask = np.where(binary_mask == 1)

        return {'outliers_mask': outliers_mask, 'binary_mask': binary_mask}

    monkeypatch.setattr(OffsetsLayer, '__init__', f_init)
    monkeypatch.setattr(OffsetsLayer, 'identify_outliers', f_identify_outliers)
    monkeypatch.setattr(OffsetsLayer, 'offsets_az',
                        np.random.randn(rester_dim[0], rester_dim[1]))
    monkeypatch.setattr(OffsetsLayer, 'offsets_rg',
                        np.random.randn(rester_dim[0], rester_dim[1]))
    monkeypatch.setattr(OffsetsLayer, 'g_offsets_az',
                        np.random.randn(rester_dim[0], rester_dim[1]))
    monkeypatch.setattr(OffsetsLayer, 'g_offsets_rg',
                        np.random.randn(rester_dim[0], rester_dim[1]))

    layer_1 = OffsetsLayer(pathlib.Path('.'))
    layer_2 = OffsetsLayer(pathlib.Path('.'))
    layer_3 = OffsetsLayer(pathlib.Path('.'))

    fill_outliers_holes(layer_1, layer_2, layer_3, {},
                        fill_strategy='median', krn_size=(9, 9))

