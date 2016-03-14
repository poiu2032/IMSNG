from astropy.io import ascii
import os
import sys
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
from astropy.time import Time
from astropy.io import ascii
from astropy.table import Table, Column
from astropy.io.votable import parse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import interpolate
from pyraf import iraf

inputlist  = 'fwhm.txt'
inlist     = ascii.read(inputlist)
inim       = inlist['filename']
fwhm       = inlist['fwhm'] 
zp         = inlist['zp']
zperr      = inlist['zperr']
starnumber = inlist['starnumber']


def gauss(group,output,sigma):
#	group=(",".join(group))
#	output=
#	combine=average
	iraf.gauss.setParam('input',group)
	iraf.gauss.setParam('output',output)
	iraf.gauss.setParam('sigma',sigma)
	iraf.gauss.setParam('nsigma','8')
#	iraf.gauss.setParam('combine',combine)
#	iraf.gauss.setParam('combine','average')
#	iraf.gauss.setParam('reject','minmax')
	iraf.gauss(group,output,sigma)

def sub(im,sub,out):
	iraf.imutil()
	iraf.imutil.imarith.setParam('operand1',im)
	iraf.imutil.imarith.setParam('op','-')
	iraf.imutil.imarith.setParam('operand2',sub)
	iraf.imutil.imarith.setParam('result',out)
	iraf.imutil.imarith(mode='h')

def multiple(im,num,out):
	iraf.imutil()
	iraf.imutil.imarith.setParam('operand1',im)
	iraf.imutil.imarith.setParam('op','*')
	iraf.imutil.imarith.setParam('operand2',num)
	iraf.imutil.imarith.setParam('result',out)
	iraf.imutil.imarith(mode='h')


os.system('rm -rf convl*.fits')
os.system('rm -rf subl*.fits')


sigmavar=[]

idx1=len(inim)-1
for i in range(len(inim)-1) :
	inim1='r'+inim[i]
	scale=10.**((zp[idx1]-zp[i]) /2.5)
	smoothing=((fwhm[i])**2. - (fwhm[idx1])**2.)
	if smoothing < 0 :
		sigma=np.sqrt((smoothing * -1.)) /2.35
		multiple(inim1,scale,'tmp.fits')
		gauss('tmp.fits','conv'+inim1,sigma)
		#gauss(inim1,'conv'+inim1,sigma)
		sub('conv'+inim1,'ref.fits','sub'+inim1)
		os.system('rm tmp.fits')
		sigmavar.append(sigma * -1.)
		print inim1,sigma * -1
	else :
		sigma=np.sqrt(smoothing) / 2.35        		
		multiple(inim1,scale,'tmp.fits')		
		gauss('ref.fits','conv'+inim1,sigma)
		#gauss('ref.fits','conv'+inim1,sigma)
		sub(inim1,'conv'+inim1,'sub'+inim1)
		os.system('rm tmp.fits')
		sigmavar.append(sigma)
		print inim1,sigma
print 'all done'
os.system('ds9 sub*.fits &')


