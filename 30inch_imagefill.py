# file transformation code for 30 inch data
# change sub region file to whole image
# ex) 200:600,1:2048 => 1:2048,1:2048

import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np
import os

backval=5000

curdir=os.getcwd()
flist=os.listdir(curdir)
fitslist=[]
for name in flist : 
	if (name[-4:]=='fits') & (name[:2]=='20'):
		fitslist.append(name)
imlist=[]		
for im in fitslist :
	if os.path.getsize(im) < 8000000L :
		imlist.append(im)
		
def fill_im(im):

	hdr=fits.getheader(im)
	data=fits.getdata(im)

	biassec=hdr['biassec']
	trimsec=hdr['trimsec']
	datasec=hdr['datasec']
	ccdsec=hdr['ccdsec']

	hdr['naxis1']=long(2080)
        hdr['naxis2']=long(2048)
        hdr['biassec']='[2057:2072,2:2047]'
        hdr['trimsec']='[2:2047,2:2047]'
        hdr['datasec']='[1:2048,1:2048]' # it must be changed, other parameter is irrelevant but just for mtching with full frame image's header
        hdr['ccdsec']='[1:2048,1:2048]'

		
	
	ccdsecx1=int(ccdsec[1:-1].split(',')[0].split(':')[0])
	ccdsecx2=int(ccdsec[1:-1].split(',')[0].split(':')[1])
	ccdsecy1=int(ccdsec[1:-1].split(',')[1].split(':')[0])
	ccdsecy2=int(ccdsec[1:-1].split(',')[1].split(':')[1])

	print 'data shape',data.shape
	print 'data dtype',data.dtype

	print ccdsec
	nd=np.full((2048,2048),5000,dtype=data.dtype)

	for y in range(ccdsecx1,ccdsecx2):
		for x in range(ccdsecy1,ccdsecy2+1) : 
			nd[x,y]=data[x-(ccdsecy1),y]

	fits.writeto('n'+im,nd,header=hdr)		
	
for im in imlist : fill_im(im)	
