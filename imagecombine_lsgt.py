#read list and make images combined for oneday 3 fits files
#mean exposure start time will be update to DATE-OBS keyword in combined image header
#python imagecombine.py

from astropy.io import ascii
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table, Column
from astropy.time import Time
from pyraf import iraf
import os, sys
import numpy as np
import matplotlib.pyplot as plt
#import ds9

os.system('rm *_com.fits')
os.system('gethead recCalibrate*.fits DATE-OBS > obj.list.date')
filename='obj.list.date'
colnames=('files','obstime')
info=ascii.read(filename,Reader=ascii.NoHeader,names=colnames)
##	info=np.loadtxt(filename)
info=Table(info)
info.sort('obstime')
files=info['files']
obstime=info['obstime']

def imcombine(group,output):
	group=(",".join(group))
#	combine=average
	iraf.imcombine.setParam('input',group)
	iraf.imcombine.setParam('output',output)
	iraf.imcombine.setParam('combine','median')
#	iraf.imcombine.setParam('combine',combine)
#	iraf.imcombine.setParam('combine','average')
	iraf.imcombine.setParam('reject','none')
	iraf.imcombine.setParam('zero','mode')
	iraf.imcombine(group,output=output)


obsdt=[]
for n in range(len(files)):
	header=fits.getheader(files[n])
	hobsdate=header['DATE-OBS']
	obsdt.append(hobsdate)
	print hobsdate	+'\n'

#time conversion to mjd
t = Time(obstime, format='isot', scale='utc')
tjd=t.mjd
#-------------------------------------------------------------
#center time calculation and put it to header
def centertimeheader(inim,putim) :	
	obsdt=[]
	for n in range(len(inim)):
		header=fits.getheader(inim[n])
		hobsdate=header['DATE-OBS']
		obsdt.append(hobsdate)
	tt = Time(obsdt, format='isot', scale='utc')
	ttjd=tt.jd
	ttjdmean=np.mean(ttjd)
		
	print ttjd
	print ttjdmean
	ttjdmeanutc=Time(ttjdmean,format='jd',scale='utc')
	
	putdata,putheader=fits.getdata(putim, header=True)
	os.system('rm '+putim)
	putheader['DATE-OBS']=ttjdmeanutc.isot
	fits.writeto(putim, putdata, putheader, clobber=True)
#---------------------------------------------------------------

com=[]
for i in range(len(files)) :
	#com.append(files[i])
	if i==0 : com.append(files[0])
	
	else :
		# if time between two exposures less than 10 min, then append new file to group	successive files will be combined together	
		if (tjd[i]-tjd[i-1]) < (10/1440.) :	
			com.append(files[i])
		else :
			
			if len(com) == 1 :
				output=com[0][:-5]+'_'+str(len(com))+'_com.fits'
				print 'these ',str(len(com)),' files will be combined ',com,' output = ',output+'\n'
				os.system('cp '+com[0]+' '+output)				
				com=[]
				com.append(files[i])
				
			else : 
				output=com[0][:-5]+'_'+str(len(com))+'_com.fits'
				imcombine(com,output)
				centertimeheader(com,output)
				print 'these ',str(len(com)),' files will be combined ',com,' output = ',output+'\n'
				com=[]
				com.append(files[i])


output=com[0][:-5]+'_'+str(len(com))+'_com.fits'			
imcombine(com,output)

print 'all done, check it out \n'

