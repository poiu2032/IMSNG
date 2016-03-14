import os
import sys
import glob
import astropy.io.fits as fits
import astropy.io.ascii as ascii
import numpy as np
from pyraf import iraf 


os.system('ls zero*.fits > zero.list')
zerolist=glob.glob('zero*.fits')
os.system('ls obj*.fits > obj.list')
objlist=glob.glob('obj*.fits')
os.system('ls ef*.fits mf*.fits > flat.list')
eflatlist=glob.glob('ef*.fits')
mflatlist=glob.glob('mf*.fits')
flatlist=eflatlist+mflatlist
os.system('ls dark*.fits > dark.list')
darklist=glob.glob('dark*.fits')


def zerocor(zerolist) :	
	
	
def imcombine(group,output):
	group=(",".join(group))
#	combine=average
	iraf.imcombine.setParam('input',group)
	iraf.imcombine.setParam('output',output)
	iraf.imcombine.setParam('combine','average')
	iraf.imcombine.setParam('scale','none')
	iraf.imcombine.setParam('zero','mode')
#	iraf.imcombine.setParam('project','no')
#	iraf.imcombine.setParam('combine',combine)
#	iraf.imcombine.setParam('combine','average')
	iraf.imcombine.setParam('reject','minmax')
	iraf.imcombine(group,output=output)

