"""
Enrico Ciraci 03/2022
Load AMPCOR Offsets Layers
"""
import os
import pathlib
from osgeo import gdal
from dataclasses import dataclass
import matplotlib.pyplot as plt
from utils.mpl_utils import add_colorbar
# - change matplotlib default setting
plt.rc('font', family='monospace')
plt.rc('font', weight='bold')
plt.style.use('seaborn-deep')


@dataclass()
class OffsetsLayer:
    """Load AMPCOR Offsets Layers"""
    def __init__(self, d_path: pathlib.Path):
        # - class attributes
        self.path = d_path          # - Absolute Path to Offsets Layer
        self.offsets_az = None      # - Dense Offsets Azimuth
        self.offsets_rg = None      # - Dense Offsets Range
        self.offsets_hdr = {}       # - Dense Offsets Metadate
        self.g_offsets_az = None    # - Gross Offsets Azimuth
        self.g_offsets_rg = None    # - Gross Offsets Range
        self.g_offset_hdr = {}      # - Gross Offsets Metadata
        self.snr = None             # - SNR
        self.snr_hdr = {}           # - SNR Header
        self.cov_az = None          # - Covariance Azimuth
        self.cov_rg = None          # - Covariance Range
        self.cov_hdr = {}           # - Covariance Header

        # - Read Offsets file
        ds = gdal.Open(str(os.path.join(d_path, 'dense_offsets')),
                       gdal.GA_ReadOnly)
        self.offsets_az = ds.GetRasterBand(1).ReadAsArray()
        self.offsets_rg = ds.GetRasterBand(2).ReadAsArray()
        ds = None
        # - Read Dense Offsets header
        with open(os.path.join(d_path, 'dense_offsets.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self.offsets_hdr[s_line[0].strip] = s_line[1].strip

        # - Read Gross Offsets file
        ds = gdal.Open(str(os.path.join(d_path, 'gross_offsets')),
                       gdal.GA_ReadOnly)
        self.g_offsets_az = ds.GetRasterBand(1).ReadAsArray()
        self.g_offsets_rg = ds.GetRasterBand(2).ReadAsArray()
        ds = None
        # - Read Dense Offsets header
        with open(os.path.join(d_path, 'gross_offsets.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self.g_offset_hdr[s_line[0].strip] = s_line[1].strip

        # - Read SNR file
        ds = gdal.Open(str(os.path.join(d_path, 'snr')),
                       gdal.GA_ReadOnly)
        self.snr = ds.GetRasterBand(1).ReadAsArray()
        ds = None
        # - Read SNR header
        with open(os.path.join(d_path, 'snr.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self.snr_hdr[s_line[0].strip] = s_line[1].strip

        # - Read Covariance file
        ds = gdal.Open(str(os.path.join(d_path, 'covariance')),
                       gdal.GA_ReadOnly)
        self.cov_az = ds.GetRasterBand(1).ReadAsArray()
        self.cov_rg = ds.GetRasterBand(2).ReadAsArray()
        ds = None
        # - Read SNR header
        with open(os.path.join(d_path, 'covariance.hdr'), 'r',
                  encoding='utf8') as h_fid:
            h_line = h_fid.readlines()
            for ln in h_line[1:]:
                s_line = ln.split('=')
                self.cov_hdr[s_line[0].strip] = s_line[1].strip

    def show_offsets(self, fig_size: tuple = (10, 6),
                     offsets_range: tuple = (-20, 20),
                     cov_range: tuple = (0, 50),
                     off_cmap: plt.cm = plt.get_cmap('viridis'),
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
        im_1 = ax_1.imshow(self.offsets_az.T, cmap=off_cmap,
                           vmin=offsets_range[0], vmax=offsets_range[1])
        add_colorbar(ax_1, im_1)

        # - Dense Offsets Range
        ax_2 = fig.add_subplot(222)
        ax_2.set_title('Offsets Range', loc='left', weight='bold')
        im_2 = ax_2.imshow(self.offsets_rg.T, cmap=off_cmap,
                           vmin=offsets_range[0], vmax=offsets_range[1])
        add_colorbar(ax_2, im_2)

        # - Covariance Offsets Azimuth
        ax_3 = fig.add_subplot(223)
        ax_3.set_title('Covariance Offsets Azimuth', loc='left', weight='bold')
        im_3 = ax_3.imshow(self.cov_az.T, cmap=cov_cmap,
                           vmin=cov_range[0], vmax=cov_range[1])
        add_colorbar(ax_3, im_3)

        # - Covariance Offsets Range
        ax_4 = fig.add_subplot(224)
        ax_4.set_title('Covariance Offsets Range', loc='left', weight='bold')
        im_4 = ax_4.imshow(self.cov_rg.T, cmap=cov_cmap,
                           vmin=cov_range[0], vmax=cov_range[1])
        add_colorbar(ax_4, im_4)
        plt.tight_layout()
        plt.show()
        plt.close()
