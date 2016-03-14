from astropy.io import ascii
import os
import sys
from astropy.io import fits
import numpy as np
from astropy.time import Time
from astropy.table import Table, Column
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
from scipy import interpolate
"""
[('filename', 'S12'), ('jd', '<f8'), ('magat', '<f8'), ('magaterr', '<f8'), ('magap5', '<f8'), ('magap5err', '<f8'), ('magap7', '<f8'), ('magap7err', '<f8'), ('sub', '<f8'), ('cmag', '<f8'), ('zperr', '<f8'), ('wmean', '<f8'), ('werr', '<f8')])
"""
photdata1=ascii.read('/home/changsu/Documents/PG0934+013/PHOTOMETRY/photresult_lcogt.txt')
photdata2=ascii.read('/home/changsu/Documents/PG0934+013/PHOTOMETRY/photresult_loao.txt')

### sorting

photdata1=Table(photdata1)
photdata2=Table(photdata2)
photdata1.sort('jd')
photdata2.sort('jd')
 sub cmag zperr wmean werr fwhm
jd1=photdata1['jd']
jd2=photdata2['jd']
amag1=photdata1['magat']
amag2=photdata2['magat']
amagerr1=photdata1['magaterr']
amagerr2=photdata2['magaterr']

mag7ap1= photdata1['magap7']
mag7ap2= photdata2['magap5']
mag7ap1err=photdata1['magap7err']
mag7ap2err=photdata2['magap5err']

werr1=photdata1['werr']
werr2=photdata2['werr']
cmag1=photdata1['cmag']
cmag2=photdata2['cmag']
amagerr1=photdata1['magaterr']
amagerr2=photdata2['magaterr']

cmag_mean=( np.mean(cmag1)+np.mean(cmag2) )/2.

sub=np.mean(amag1) - np.mean(amag2)
sub=0.14
### error

terr1=np.sqrt(werr1**2 + amagerr1**2)
ferr=np.sqrt(sum(terr1**2)/(len(terr1)-1))
terr2=np.sqrt(werr2**2 + amagerr2**2)
lerr=np.sqrt(sum(terr2**2)/(len(terr2)-1))
err=np.sqrt((ferr**2 + lerr**2)/2)

print 'front, back, total,', "%.4f" % ferr, "%.4f" % lerr, "%.4f" % err

### interpolation
xi1 = np.linspace(np.min(jd1), np.max(jd1), len(jd1)*4.)
ius1=InterpolatedUnivariateSpline(jd1, amag1)
yi1=ius1(xi1)
xi2 = np.linspace(np.min(jd2), np.max(jd2), len(jd2)*4.)
ius2=InterpolatedUnivariateSpline(jd2, amag2)
yi2=ius2(xi2)


### rbf
xi2 = np.linspace(np.min(jd2), np.max(jd2), len(jd2)*4.)
rbf = Rbf(jd2, amag2)
fi2 = rbf(xi2)
#plt.plot(xi2, fi2, 'b')

#xi1 = np.linspace(np.min(jd1), np.max(jd1), len(jd1)*4.)
#rbf = Rbf(jd1, amag1)
#fi1 = rbf(xi1)
#plt.plot(xi1, fi1, 'b')

xi2 = np.linspace(np.min(jd2), np.max(jd2), len(jd2)*4)
f = interpolate.interp1d(jd2, amag2)
ynew=f(xi2)


x=[np.min(jd1),np.max(jd2)]
y=[cmag_mean,cmag_mean]
plt.plot(x,y)

#plt.plot(xi2,yi2,'g')
plt.plot(jd1,amag1-sub,'.')
plt.plot(jd2,amag2,'.')
plt.plot(jd1,cmag1,'.')
plt.plot(jd2,cmag2,'.')
plt.plot(xi2, ynew, 'r')

plt.grid()
plt.show()



