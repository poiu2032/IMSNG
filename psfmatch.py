#python psfmatch.py obj.list
#psfexrun.py first, need psf~.fits file
#convolution(pm~) and flux scaling(fs~) together
#subtraction (sub~)

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

def psfmatch(im,impsf,out) :
	iraf.immatch()
	iraf.immatch.psfmatch.setParam('input',im)
	iraf.immatch.psfmatch.setParam('reference',impsf)
	iraf.immatch.psfmatch.setParam('psfdata','psfref.fits')
	iraf.immatch.psfmatch.setParam('output',out)
	iraf.immatch.psfmatch.setParam('convolution','psf')
	iraf.immatch.psfmatch(mode='h')

def linmatch(im,ref,out) :
	iraf.immatch()
	iraf.immatch.linmatch.setParam('input',im)
	iraf.immatch.linmatch.setParam('reference',ref)
	iraf.immatch.linmatch.setParam('regions','[500:1500,500:1500]')
	iraf.immatch.linmatch.setParam('lintrans','linmatch.db')
	iraf.immatch.linmatch.setParam('output',out)
	iraf.immatch.linmatch.setParam('scaling','fit')
	iraf.immatch.linmatch(mode='h')

os.system('ls resac*.fits > obj.list')
os.system('rm sub*.fits')
os.system('rm pm*.fits')
os.system('rm fs*.fits')
tmpin  = np.genfromtxt('obj.list',usecols=(0),dtype=str)
inim   = list(tmpin)

for images in inim :
	impsf = 'psf'+images
	out   = 'pm'+images
	psfmatch('ref.fits',impsf,out)
	linmatch(out,images,'fs'+out) 
	sub(images,'fs'+out,'sub'+images)

print 'all done, Let\'s see the result !! \n'
os.system('ds9 sub*.fits &')
