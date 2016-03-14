import numpy as np
from photutils import datasets
import pandas as pd
import astropy.io.fits as fits
from photutils import daofind
from astropy.stats import mad_std
from photutils import aperture_photometry, CircularAperture
import matplotlib.pylab as plt
import scikit-image as scim
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy.visualization import SqrtStretch
from photutils import detect_threshold


data='tt.fits'
im=fits.getdata(data)
im.astype(float) - np.median(im)
bkg_sigma = mad_std(im) 
sources = daofind(im, fwhm=11., threshold=3.*bkg_sigma)
print(sources)

positions = (sources['xcentroid'], sources['ycentroid']) 
apertures = CircularAperture(positions, r=11,error=data_err)
apertures = 
phot_table = aperture_photometry(im, apertures) 
print(phot_table) 
plt.imshow(im, cmap='gray_r', origin='lower',norm=norm)#,vmin=0,vmax=100)
norm = ImageNormalize(stretch=sqrtStretch())
apertures.plot(color='blue', lw=1.5, alpha=0.5)
plt.show()
plt.close()

threshold = detect_threshold(data, snr=3.)

