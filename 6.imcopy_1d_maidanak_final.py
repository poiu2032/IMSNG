# Edit image
from astropy.io import fits
import os
import sys
import numpy as np
from pyraf import iraf


#os.system('rm t*.fits')
os.system('ls -d m* ngc* M* NGC* messier* IC* CGC* ic* ugc* UGC* PGC* MGC* IRAS* > direc.list')
alllist=np.genfromtxt('direc.list',usecols=(0),dtype=str)
for i in range(len(alllist)) :
	os.chdir(alllist[i])
	os.system('ls bgfz*.fits  > obj.list')
	objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
	objlist=list(objlist)


	def imtrim(im) :
		data=fits.getdata(im)
		hdr=fits.getheader(im)
		newdata=data[0][60:-60,6:-6]
		hdr['COMMENT']='trimmed from '+im
		hdr['COMMENT']='[6:4090 , 60:4036]'
		fits.writeto('t'+im, newdata, hdr, clobber=True)
		print im, 'will be trimmed to','t'+im 
	for im in objlist : imtrim(im)
	os.chdir('../')

print 'All images are trimmed.'
os.system('python /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/7.fnamechange_1d_maidanak.py')



'''  ## IRAF imcopy task method
for im in objlist :
    inim=im+'[6:, 60:]'
    im.split('/')
    outim=im.split('/')[0]+'/t'+im.split('/')[1]
    iraf.imcopy(inim,outim)
'''
