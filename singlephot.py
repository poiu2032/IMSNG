# one point photometry using source extractor and APASS catalog
# LSGT data only
# python singlephot.py 
#/data0/itelescope_data/t52/ATEL7987/com/R

import os
import sys
import numpy as np
from astropy.io import fits
from astropy.io import ascii
from astropy.time import Time
import astropy.units as u
import astropy.coordinates as coord
from astropy.io.votable import parse
from astropy.table import Table, Column
import robust
import string
import math
import pylab as pl
import glob
from PIL import Image
from matplotlib import pyplot as mpl
import subprocess
import aplpy




# location of target in deg, single target!!
locx = 246.50883 
locy = -27.30411



objmag    = []
objmagerr = []

dirhere = os.getcwd()
dirhere = dirhere.split('/') 
outfile = dirhere[4]+'-'+dirhere[6]+'-phot.txt'
#refcat  = '../apass_'+dirhere[4]+'.cat'
refcat  = '../photref.cat'

os.system('ls cCal*.fits > obj.list')
inlist = np.genfromtxt('obj.list',usecols=(0),dtype=str)
inlist = list(inlist)

filters      = ['Johnson_B','Johnson_V','convert_R']
errors       = ['B_err','Verr','convert_Rerr']
filtershere  = ['B','V','R']
errname      = errors[filtershere.index(dirhere[6])]
filname      = filters[filtershere.index(dirhere[6])] 

## source extractor parameter
apersize     = '6,10,14'  # 3", 5", 7" aperture
 # x pix scale 0.5
detecthred   = '2'
analthred    = '2'
os.system('cp /data0/code/sex.config/snphot.* .')


#fwhmzp=ascii.read('fwhm.txt')
objatmag,objatme = [],[]
obja3mag,obja3me = [],[]
obja5mag,obja5me = [],[]
obja7mag,obja7me = [],[]
zpat,zpate=[],[]
zpa3,zpa3e=[],[]
zpa5,zpa5e=[],[]
zpa7,zpa7e=[],[]
numat,numap3,numap5,numap7=[],[],[],[]



for im in inlist : 

# find zp for auto ap3, ap7
	mcat=im[:-5]+'.merge.cat'
	mcat=ascii.read(mcat)
	sra =mcat['col4'] 
	sdec=mcat['col5']
	
	atmag, atme = mcat['col8'], mcat['col9']   
	a3mag, a3me = mcat['col43'],mcat['col53'] 
	a7mag, a7me = mcat['col47'],mcat['col57']
	
	refmag, refme = mcat[filname],mcat[errname]
	stnum=len(refmag)
	aval=robust.mean(refmag - atmag ,Cut=3.0)    #zp and error for one image
	zpat.append(aval[0])
	zpate.append(aval[1])	
	
	aval=robust.mean(refmag - a3mag ,Cut=3.0)    #zp and error for one image
	zpa3.append(aval[0])
	zpa3e.append(aval[1])	

	aval=robust.mean(refmag - a7mag ,Cut=3.0)    #zp and error for one image
	zpa7.append(aval[0])
	zpa7e.append(aval[1])	


# for each input image, calculate magnitude
	i=inlist.index(im)
	incat=im[:-5]+'.cat'
	incat=ascii.read(incat)
	sra =incat['col4'] 
	sdec=incat['col5']
	
	inatmag,inatme=incat['col8'],incat['col9']
	ina3mag,ina3me=incat['col43'],incat['col53']
	ina7mag,ina7me=incat['col47'],incat['col57']

	dist=np.sqrt((sra-locx)**2+ (sdec-locy)**2)
	idx=np.where((dist < (1/3600.)) & (dist==min(dist)))
	idx=idx[0][0]
	objatmag.append((inatmag[idx]+zpat[i]))
	objatme.append((np.sqrt(inatme[idx]**2 +zpate[i]**2)))

	obja3mag.append((ina3mag[idx]+zpa3[i]))
	obja3me.append((np.sqrt(ina3me[idx]**2 +zpa3e[i]**2)))

	obja7mag.append((ina7mag[idx]+zpa7[i]))
	obja7me.append((np.sqrt(ina7me[idx]**2 +zpa7e[i]**2)))


k=open(outfile,'w')
tt=[]
k.write('# filename	obsdate	mjd	starnum	automag	automagerr	ap3mag	ap3magerr	ap7mag	ap7magerr\n')
for i in range(len(inlist)) :
		inimage = inlist[i]
		head    = fits.getheader(inimage)
		obsdate = head['DATE-OBS']
		t       = Time(obsdate, format='isot', scale='utc')
		tjd     = t.mjd
		tt.append(tjd)
		print tjd, stnum, obja3mag[i], obja3me[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
		#comment = str(tjd)+'\t'+str(list(snmag[i]))+'\t'+str(list(snmagerr[i]))+'\n'
		comment = inimage+'\t'+obsdate+'\t'+str(tjd)+'\t'+str(stnum)+'\t'+ '%.3f' % objatmag[i]+'\t'+'%.3f' % objatme[i]+'\t'+'%.3f' %obja3mag[i]+'\t'+'%.3f' % obja3me[i]+'\t'+'%.3f' % obja7mag[i]+'\t'+'%.3f' % obja7me[i]+'\n'
		k.write(comment)

k.close()
















