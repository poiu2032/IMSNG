# Edit image
from astropy.io import fits
import os
import sys
import numpy as np
from pyraf import iraf


os.system('rm tbg*.fits')
os.system('ls bgfz*.fits  > obj.list')
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
objlist=list(objlist)


def imtrim(im) :
	data=fits.getdata(im)
	hdr=fits.getheader(im)
	newdata=data[0][60:-60,6:-6]
	hdr['COMMENT']='trimmed from'+im
	hdr['COMMENT']='[6:4090 , 60:4036]'
	fits.writeto('t'+im, newdata, hdr, clobber=True)
	print im, 'will be trimmed to','t'+im 

n=0
for im in objlist : 
	imtrim(im)
	n=n+1
	print n,'th file of ',len(objlist)  	




'''  ## IRAF imcopy task method
for im in objlist :
    inim=im+'[6:, 60:]'
    im.split('/')
    outim=im.split('/')[0]+'/t'+im.split('/')[1]
    iraf.imcopy(inim,outim)
'''
