from astropy.io import ascii
import os
import sys
from astropy.io import fits
import numpy as np
from astropy.time import Time
from astropy.io.votable import parse
import matplotlib.pyplot as plt
from scipy import interpolate
from astropy.io.votable import parse
import matplotlib.cm as cm


os.system("sex -c phot.sex -psf_name rasassn-lp.r.psf rasassn-lp.r.fits")


cat=ascii.read('test.cat')

ap1=cat['MAG_APER']
ap2=cat['MAG_APER_1']
ap3=cat['MAG_APER_2']
ap4=cat['MAG_APER_3']
ap5=cat['MAG_APER_4']
ap6=cat['MAG_APER_5']
ap7=cat['MAG_APER_6']
ap8=cat['MAG_APER_7']
ap9=cat['MAG_APER_8']
ap10=cat['MAG_APER_9']
atmag=cat['MAG_AUTO']
psfmag=cat['MAG_PSF']

apnum=[1.,2.,3.,4.,5.,6.,7.,8.,9.,10.]


lox=493.
loy=442.

snx=cat['X_IMAGE']
sny=cat['Y_IMAGE']
dist=np.sqrt((snx-lox)**2+ (sny-loy)**2)
idx=np.where(dist==min(dist))
idx1=idx[0][0]
apmagsn=[ap1[idx1],ap2[idx1],ap3[idx1],ap4[idx1],ap5[idx1],ap6[idx1],ap7[idx1],ap8[idx1],ap9[idx1],ap10[idx1]]

atmagsn=atmag[idx1]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
for i in range(len(ap1)) :
	apmag=[ap1[i],ap2[i],ap3[i],ap4[i],ap5[i],ap6[i],ap7[i],ap8[i],ap9[i],ap10[i]]
	ax.scatter(apnum,apmag, marker='.',color='b',s=5)

ax.scatter(apnum, apmagsn,marker='o',color='r',s=10)

ax.set_xlim(0,11)
ax.set_ylim(-5,-17)

ax.set_title('aperture growth curve')
ax.set_xlabel('aperture(arcsec)')
ax.set_ylabel('instrument magnitude')
#ax.legend((['50d','squean flux']),loc='upper right')
fig.show()
fig.savefig("apergrowthcurve.pdf")
	
