"""
Enrico Ciraci 03/2022
Set of utility functions that can be used to generate figures with matplotlib.
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def add_colorbar(ax: plt.Axes, im: plt.pcolormesh) -> plt.colorbar:
    """
    Add colorbar to the selected plt.Axes.
    :param ax: plt.Axes object
    :param im: plt.pcolormesh object
    :return: plt.colorbar
    """
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cb = plt.colorbar(im, cax=cax)
    return cb

