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

photdata1=ascii.read('/home/changsu/Documents/PG0934+013/PHOTOMETRY/photresult_lcogt.txt')
photdata2=ascii.read('/home/changsu/Documents/PG0934+013/PHOTOMETRY/photresult_loao.txt')

photdata1=Table(photdata1)
photdata2=Table(photdata2)
photdata1.sort('jd')
photdata2.sort('jd')

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

cmag_mean=( np.mean(cmag1)+np.mean(cmag2) )/2.


terr1=np.sqrt(werr1**2 + amagerr1**2)
ferr=np.sqrt(sum(terr1**2)/(len(terr1)-1))
terr2=np.sqrt(werr2**2 + amagerr2**2)
lerr=np.sqrt(sum(terr2**2)/(len(terr2)-1))
err=np.sqrt((ferr**2 + lerr**2)/2)

print 'mean front, back, total,', "%.4f" % cmag_mean, "%.4f" % ferr, "%.4f" % lerr, "%.4f" % err
head='#comp_mean, LCOGT, LOAO, total error estimate , '+ "%.4f" % cmag_mean+" "+ "%.4f" % ferr+' '+ "%.4f" % lerr+' '+ "%.4f" % err + '\n'

f=open('phot_final.txt','w')
f.write(head)
f.write('#jd magap7 magap7err cmag werr obs \n')

for n in range(len(jd1)) :
	photline1=str(jd1[n]) +' '+  "%.4f" % mag7ap1[n]+' '+ "%.4f" % mag7ap1err[n] + ' ' + "%.4f" % cmag1[n] + ' '+ "%.4f" % werr1[n] + ' LCOGT'+'\n'
	f.write(photline1)

for h in range(len(jd2)) :
	photline2=str(jd2[h]) +' '+ "%.4f" % mag7ap2[h]+' '+ "%.4f" % mag7ap2err[h] + ' ' + "%.4f" % cmag2[h] + ' '+ "%.4f" % werr2[h] + ' LOAO'+'\n'
	f.write(photline2)

f.close()
colnames=['jd', 'magap7', 'magap7err', 'cmag', 'werr','obs']
photdata=ascii.read('/home/changsu/Documents/PG0934+013/PHOTOMETRY/phot_final.txt',names=colnames)
photdata=Table(photdata)

photdata.sort('jd')
ascii.write(photdata,'phot.txt')

