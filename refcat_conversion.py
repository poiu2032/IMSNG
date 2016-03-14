#python refcat_conversion.py 
#converse magnitude from reference catalog and add columns to original catalog, then make new reference catalog.
#SDSS DR9 to Bmag,Bmagerr following to the conversion equation of Lupton 2005.

import os,sys
import numpy as np
from astropy.io import ascii
from astropy.io import fits
from astropy.time import Time
from astropy.io.votable import parse
from astropy.time import Time
from astropy.table import Column
import robust
import matplotlib.pyplot as plt

'''
===========================================================================
Lupton (2005)

 These equations that Robert Lupton derived by matching DR4 photometry 
 to Peter Stetson's published photometry for stars.


   Stars

   B = u - 0.8116*(u - g) + 0.1313;  sigma = 0.0095
   B = g + 0.3130*(g - r) + 0.2271;  sigma = 0.0107  * # u-band mag error is to big, so I used this conversion equation. 

   V = g - 0.2906*(u - g) + 0.0885;  sigma = 0.0129
   V = g - 0.5784*(g - r) - 0.0038;  sigma = 0.0054

   R = r - 0.1837*(g - r) - 0.0971;  sigma = 0.0106
   R = r - 0.2936*(r - i) - 0.1439;  sigma = 0.0072

   I = r - 1.2444*(r - i) - 0.3820;  sigma = 0.0078
   I = i - 0.3780*(i - z)  -0.3974;  sigma = 0.0063

============================================================================
'''

refcat='/data1/PG0934+013/PHOTOMETRY/process/sdssref.cat'
ref=ascii.read(refcat)
# SDSS9	RAJ2000	DEJ2000	ObsDate	umag	e_umag   gmag     e_gmag   rmag     e_rmag   imag     e_imag   zmag     e_zmag 

umag,umagerr=ref['umag'],ref['e_umag']
rmag,rmagerr=ref['rmag'],ref['e_rmag']
gmag,gmagerr=ref['gmag'],ref['e_gmag']


ind=np.where((umagerr < 0.5) & (gmagerr < 0.2) & (rmagerr < 0.2))


ugBmag=umag - 0.8116*(umag - gmag) + 0.1313
ugBmagerr=np.sqrt(np.sqrt(umagerr**2 + gmagerr**2)**2 + 0.0095**2)
grBmag=gmag + 0.3130*(gmag - rmag) + 0.2271
grBmagerr=np.sqrt(np.sqrt(umagerr**2 + gmagerr**2)**2 + 0.010795**2)


Bmag=Column(grBmag,name='Bmag',format='% 1.3f')           # dtype='f2')
Bmagerr=Column(grBmagerr,name='Bmagerr',format='% 1.3f')

ref.add_column(Bmag)
ref.add_column(Bmagerr)

ascii.write(ref,'sdssref_B.cat')  ##,format='ascii',fast_writer=False)


