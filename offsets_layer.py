u"""
Enrico Ciraci 03/2022
Load AMPCOR Offsets Layers
"""
import os
import pathlib
import copy
from osgeo import gdal
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from utils.mpl_utils import add_colorbar
# - change matplotlib default setting
plt.rc('font', family='monospace')
plt.rc('font', weight='bold')
plt.style.use('seaborn-deep')


class OffsetsLayer:
    """Load AMPCOR Offsets Layers"""
    def __init__(self, d_path: pathlib.Path):
        # - class attributes
        self._path = d_path          # - Absolute Path to Offsets Layer
        self._offsets_az = None      # - Dense Offsets Azimuth
        self._offsets_rg = None      # - Dense Offsets Range
        self._offsets_hdr = {}       # - Dense Offsets Metadate
        self._g_offsets_az = None    # - Gross Offsets Azimuth
        self._g_offsets_rg = None    # - Gross Offsets Range
        self._g_offset_hdr = {}      # - Gross Offsets Metadata
        self._snr = None             # - SNR
        self._snr_hdr = {}           # - SNR Header
        self._cov_az = None          # - Covariance Azimuth
        self._cov_rg = None          # - Covariance Range
        self._cov_hdr = {}           # - Covariance Header
        self._shape = None           # - Offsets layer shape

        # - Read Offsets file
        ds = gdal.Open(str(os.path.join(d_path, 'dense_offsets')),
                       gdal.GA_ReadOnly)
        self._offsets_az = ds.GetRasterBand(1).ReadAsArray()
        self._offsets_rg = ds.GetRasterBand(2).ReadAsArray()
        self._shape = self._offsets_rg.shape
        ds = None
        # - Read Dense Offsets header
        with open(os.path.join(d_path, 'dense_offsets.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self._offsets_hdr[s_line[0].strip] = s_line[1].strip

        # - Read Gross Offsets file
        ds = gdal.Open(str(os.path.join(d_path, 'gross_offsets')),
                       gdal.GA_ReadOnly)
        self._g_offsets_az = ds.GetRasterBand(1).ReadAsArray()
        self._g_offsets_rg = ds.GetRasterBand(2).ReadAsArray()
        ds = None
        # - Read Dense Offsets header
        with open(os.path.join(d_path, 'gross_offsets.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self._g_offset_hdr[s_line[0].strip] = s_line[1].strip

        # - Read SNR file
        ds = gdal.Open(str(os.path.join(d_path, 'snr')),
                       gdal.GA_ReadOnly)
        self._snr = ds.GetRasterBand(1).ReadAsArray()
        ds = None
        # - Read SNR header
        with open(os.path.join(d_path, 'snr.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self._snr_hdr[s_line[0].strip] = s_line[1].strip

        # - Read Covariance file
        ds = gdal.Open(str(os.path.join(d_path, 'covariance')),
                       gdal.GA_ReadOnly)
        self._cov_az = ds.GetRasterBand(1).ReadAsArray()
        self._cov_rg = ds.GetRasterBand(2).ReadAsArray()
        ds = None
        # - Read SNR header
        with open(os.path.join(d_path, 'covariance.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self._cov_hdr[s_line[0].strip] = s_line[1].strip

    def __copy__(self):
        return OffsetsLayer(self._path)

    def __deepcopy__(self, memo):
        return OffsetsLayer(copy.deepcopy(self._path, memo))

    @property
    def size(self):
        """Return Offsets Maps size"""
        return self._offsets_rg.shape

    @property
    def offsets_az(self):
        """Get Offsets Azimuth Direction"""
        return self._offsets_az

    @offsets_az.setter
    def offsets_az(self, offsets_az: np.ndarray):
        """Set Offsets Azimuth Direction"""
        if offsets_az.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._offsets_az = offsets_az

    @property
    def offsets_rg(self):
        """Get Offsets Range Direction"""
        return self._offsets_rg

    @offsets_rg.setter
    def offsets_rg(self, offsets_rg: np.ndarray):
        """Set Offsets Range Direction"""
        if offsets_rg.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._offsets_rg = offsets_rg

    @property
    def g_offsets_az(self):
        """Get Gross Offsets Azimuth Direction"""
        return self._g_offsets_az

    @g_offsets_az.setter
    def g_offsets_az(self, g_offsets_az: np.ndarray):
        """Set Gross Offsets Azimuth Direction"""
        if g_offsets_az.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._g_offsets_az = g_offsets_az

    @property
    def g_offsets_rg(self):
        """Get Gross Offsets Range Direction"""
        return self._g_offsets_rg

    @g_offsets_rg.setter
    def g_offsets_rg(self, g_offsets_rg: np.ndarray):
        """Set Gross Offsets Range Direction"""
        if g_offsets_rg.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._g_offsets_rg = g_offsets_rg

    @property
    def cov_az(self):
        """Get Offsets Covariance Azimuth Direction"""
        return self._cov_az

    @cov_az.setter
    def cov_az(self, cov_az: np.ndarray):
        """Set Offsets Covariance Azimuth Direction"""
        if cov_az.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._cov_az = cov_az

    @property
    def cov_rg(self):
        """Get Offsets Covariance Range Direction"""
        return self._cov_az

    @cov_rg.setter
    def cov_rg(self, cov_rg: np.ndarray):
        """Set Offsets Covariance Range Direction"""
        if cov_rg.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._cov_rg = cov_rg

    @property
    def snr(self):
        """Get Offsets SNR"""
        return self._snr

    @snr.setter
    def snr(self, snr: np.ndarray):
        """Set Offsets SNR"""
        if snr.shape != self._shape:
            raise ValueError(': Offsets Layers Dimensions do not match.')
        self._snr = snr

    def identify_outliers(self, metric: str = 'snr', threshold: float = 1.,
                          window_az: int = 50, window_rg: int = 50,
                          ) -> dict:
        """
        Identify outliers in the offset fields.
        Outliers are identified by thresholding a
        metric (SNR, offset covariance, offset median
        absolute deviation) suggested by the user
        -------
        :param metric: outlier selection metric - str
        :param threshold: outlier selection threshold - str
        :param window_az: azimuth windows search size
        :param window_rg: range windows search size
        :return: outliers_mask - dict
        """
        if metric == 'snr':
            # - Open SNR
            outliers_mask = np.where(self._snr < threshold)

        elif metric == 'median_filter':
            # - Use offsets to compute "median absolute deviation" (MAD)
            median_az = ndimage.median_filter(self._offsets_az,
                                              [window_az, window_rg])
            median_rg = ndimage.median_filter(self._offsets_rg,
                                              [window_az, window_rg])

            outliers_mask \
                = (np.abs(self._offsets_az - median_az) > threshold) | \
                  (np.abs(self._offsets_rg - median_rg) > threshold)

        elif metric == 'covariance':
            # - Use offsets azimuth and range covariance elements
            outliers_mask = (self._cov_az > threshold) |\
                            (self._cov_rg > threshold)
        else:
            err_str = f'{metric} invalid metric to filter outliers'
            raise ValueError(err_str)

        # - outlier binary mask
        binary_mask = np.zeros(self._shape)
        binary_mask[outliers_mask] = 1

        return{'outliers_mask': outliers_mask, 'binary_mask': binary_mask}

    def mask_outliers(self, mask: np.ndarray) -> None:
        """
        Apply binary mask to Layer fields:
        - mask = 1 -> NonValid data Points - set to NaN
        - mask = 0 -> Valid data point
        ------------
        :param mask: binary mask - np.ndarray
        :return: None
        """
        if mask.shape != self._shape:
            raise ValueError(f'operands could not be broadcast '
                             f'together with shapes ({mask.shape}) '
                             f'({self._shape})')
        else:
            ind_bin = np.where(mask == 1.)
            self._offsets_az[ind_bin] = np.nan    # - Dense Offsets Azimuth
            self._offsets_rg[ind_bin] = np.nan    # - Dense Offsets Range
            self._g_offsets_az[ind_bin] = np.nan  # - Gross Offsets Azimuth
            self._g_offsets_rg[ind_bin] = np.nan  # - Gross Offsets Range
            self._snr[ind_bin] = np.nan           # - Gross Offsets Range
            self._cov_az[ind_bin] = np.nan        # - Covariance Azimuth Azimuth
            self._cov_rg[ind_bin] = np.nan        # - Covariance Azimuth Range

    def show_offsets(self, fig_size: tuple = (10, 6),
                     offsets_range: tuple = (-20, 20),
                     cov_range: tuple = (0, 50),
                     off_cmap: plt.cm = plt.get_cmap('RdBu'),
                     cov_cmap: plt.cm = plt.get_cmap('Reds')) -> None:
        """
        Show Offsets Maps
        :param fig_size: figure size - tuple
        :param offsets_range: offsets (min, max) values - tuple
        :param cov_range: covariance (min, max) values - tuple
        :param off_cmap: offsets colormap
        :param cov_cmap: covariance colormap
        :return: None
        """
        # - Show Grid Search Error Array
        fig = plt.figure(figsize=fig_size)
        # - Dense Offsets Azimuth
        ax_1 = fig.add_subplot(221)
        ax_1.set_title('Offsets Azimuth', loc='left', weight='bold')
        im_1 = ax_1.pcolormesh(self._offsets_az.T, cmap=off_cmap,
                               vmin=offsets_range[0], vmax=offsets_range[1])
        add_colorbar(ax_1, im_1)

        # - Dense Offsets Range
        ax_2 = fig.add_subplot(222)
        ax_2.set_title('Offsets Range', loc='left', weight='bold')
        im_2 = ax_2.pcolormesh(self._offsets_rg.T, cmap=off_cmap,
                               vmin=offsets_range[0], vmax=offsets_range[1])
        add_colorbar(ax_2, im_2)

        # - Covariance Offsets Azimuth
        ax_3 = fig.add_subplot(223)
        ax_3.set_title('Covariance Offsets Azimuth', loc='left', weight='bold')
        im_3 = ax_3.pcolormesh(self._cov_az.T, cmap=cov_cmap,
                               vmin=cov_range[0], vmax=cov_range[1])
        add_colorbar(ax_3, im_3)

        # - Covariance Offsets Range
        ax_4 = fig.add_subplot(224)
        ax_4.set_title('Covariance Offsets Range', loc='left', weight='bold')
        im_4 = ax_4.pcolormesh(self._cov_rg.T, cmap=cov_cmap,
                               vmin=cov_range[0], vmax=cov_range[1])
        add_colorbar(ax_4, im_4)
        plt.tight_layout()
        plt.show()
        plt.close()

    def plot_offsets_distribution(self, fig_size: tuple = (10, 4),
                                  offsets_range: tuple = (-20, 20),
                                  n_bins: int = 41,
                                  density: bool = True) -> None:
        """
        Plot Histograms showing Offsets value distribution.
        :param fig_size: figure size
        :param offsets_range: histogram x-axis limits
        :param n_bins: histogram number of bins
        :param density: If True, draw and return offstets probability density
        :return: None
        """
        # - Show Grid Search Error Array
        fig = plt.figure(figsize=fig_size)
        # - Dense Offsets Azimuth
        ax_1 = fig.add_subplot(121)
        ax_1.set_title('Offsets Azimuth', loc='left', weight='bold')
        ax_1.hist(self._offsets_az.ravel(), n_bins, density=density,
                  facecolor='g', edgecolor='k', alpha=0.75)
        ax_1.grid(color='k', linestyle='dotted', alpha=0.3)
        ax_1.set_xlim(offsets_range[0], offsets_range[1])

        # - Dense Offsets Range
        ax_2 = fig.add_subplot(122)
        ax_2.set_title('Offsets Range', loc='left', weight='bold')
        ax_2.hist(self._offsets_rg.ravel(), n_bins, density=density,
                  facecolor='b', edgecolor='k', alpha=0.75)
        ax_2.grid(color='k', linestyle='dotted', alpha=0.3)
        ax_2.set_xlim(offsets_range[0], offsets_range[1])

        plt.tight_layout()
        plt.show()
        plt.close()
