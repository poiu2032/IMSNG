# one point photometry using source extractor and APASS catalog
# LSGT data only
# python singlephot.py 
# /data0/itelescope_data/t52/ATEL7987/com/R

# detection.fits
# sextractor threshold, aperture, seeing
# outradius and inradius of reference catalog
# path of data directory
# location of target
# reference catalog



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
locx = 14.949292
locy = -7.5718333
'''
try : 
	os.listdir('detection.fits')
	print '\n Check the location of target and other parameters'
except : 
	print '\n No detection.fits'
	print ' Make a detection.fits and run me again.' 
	sys.exit()
'''


objmag    = []
objmagerr = []

dirhere = os.getcwd()
dirhere = dirhere.split('/') 
outfile = dirhere[3]+'-'+dirhere[6]+'-phot.txt'    ##  'NGC0337-R-phot.txt'
refcat  = '../apass_'+dirhere[3]+'.cat'            ##  ex) ../apass_NGC0337.cat
#refcat  = '../photref.cat'

os.system('ls recCal*.fits > obj.list')
inlist = np.genfromtxt('obj.list',usecols=(0),dtype=str)
inlist = list(inlist)

filters      = ['Johnson_B','Johnson_V','convert_R']
errors       = ['B_err','Verr','convert_Rerr']
filtershere  = ['B','V','R']
errname      = errors[filtershere.index(dirhere[6])]
filname      = filters[filtershere.index(dirhere[6])] 

## source extractor parameter
os.system('cp /data0/code/sex.config/snphot* .' )
 # x pix scale 0.5

### sextractor dual mode, detection.fits is fine image shows target significantly and has good seeing and many stars in it.
def sedual(measure) : 
	print 'Dual mode souce extractror is running on', measure
	detecthred   = '1.2'        ## sextractor parameter first for LSGT
	analthred    = '2'
	seeing       = '2.5'
	apersize     = '6,10,14'  # 3", 5", 7" aperture
	detect='detection.fits'	  ## detection.fits is fine image show target significantly and have good seeing and many stars in it.
	sedualcom='sex -c snphot.sex '+detect+' , '+measure+' -CATALOG_NAME dual'+measure[:-5]+'.cat -SEEING_FWHM '+seeing+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred #+' -PHOT_APERTURES '+apersize 
	os.system(sedualcom)
	print 'Output catalog is : ','dual'+measure[:-5]+'.cat'
	


# ready for variables
objatmag,objatme = [],[]
obja3mag,obja3me = [],[]
obja5mag,obja5me = [],[]
obja7mag,obja7me = [],[]
zpat,zpate=[],[]
zpa3,zpa3e=[],[]
zpa5,zpa5e=[],[]
zpa7,zpa7e=[],[]
numat,numap3,numap5,numap7=[],[],[],[]


# find zp for auto ap3, ap5, ap7 from dualrecCal~~.fits
def zpcal(im) :
	mcat='dual'+im[:-5]+'.merge.cat'
	mcat=ascii.read(mcat)
	sra =mcat['col4'] 
	sdec=mcat['col5']
	stel=mcat['col15']
	flag=mcat['col14'] 
	atmag, atme = mcat['col6'], mcat['col7']  
	a3mag, a3me = mcat['col8'], mcat['col9'] 
	a5mag, a5me = mcat['col10'],mcat['col11']  
	a7mag, a7me = mcat['col12'],mcat['col13']

	outradius=7/60.	 ## arcmin unit
	inradius= 1/60.
	dist=np.sqrt((sra-locx)**2+ (sdec-locy)**2)
	index=np.where((dist > inradius) & (dist < outradius) & (atme < 0.2) ) #& (flag < 5) )  ## inside ouradius and outside inradius
	index=list(index[0])
	print len(index)
	
	refmag, refme = mcat[filname],mcat[errname]
	
	stnum=len(refmag)
	aval=robust.mean(refmag[index] - atmag[index] ,Cut=3.0)    #zp and error for one image
	zpat,zpate = aval[0],aval[1]
	#zpat.append(aval[0])
	#zpate.append(aval[1])	
	aval=robust.mean(refmag[index] - a3mag[index] ,Cut=3.0)    #zp and error for one image
	zpa3,zpa3e = aval[0],aval[1]
	#zpa3.append(aval[0])
	#zpa3e.append(aval[1])	
	
	aval=robust.mean(refmag[index] - a5mag[index] ,Cut=3.0)    #zp and error for one image
	zpa5,zpa5e = aval[0],aval[1]
	#zpa3.append(aval[0])
	#zpa3e.append(aval[1])	

	aval=robust.mean(refmag[index] - a7mag[index] ,Cut=3.0)    #zp and error for one image
	zpa7,zpa7e = aval[0],aval[1]
	#zpa3.append(aval[0])
	#zpa3e.append(aval[1])	

	# for each input image, calculate magnitude of target from hdrecCal~~.fits
	incat='dualhd'+im[:-5]+'.cat'
	incat=ascii.read(incat)
	sra =incat['ALPHA_J2000'] 
	sdec=incat['DELTA_J2000']

	inatmag,inatme=incat['MAG_AUTO'],incat['MAGERR_AUTO']
	ina3mag,ina3me=incat['MAG_APER'],incat['MAGERR_APER']
	ina5mag,ina5me=incat['MAG_APER_1'],incat['MAGERR_APER_1']
	ina7mag,ina7me=incat['MAG_APER_2'],incat['MAGERR_APER_2']

	dist=np.sqrt((sra-locx)**2+ (sdec-locy)**2)

	try :
		idx=np.where((dist < (2/3600.)) & (dist==min(dist)))
		idx=idx[0][0]
		objatmag = inatmag[idx]+zpat
		objatme  = np.sqrt(inatme[idx]**2 + zpate**2)	
		obja3mag = ina3mag[idx]+zpa3
		obja3me  = np.sqrt(ina3me[idx]**2 + zpa3e**2)
		obja5mag = ina5mag[idx]+zpa5
		obja5me  = np.sqrt(ina5me[idx]**2 + zpa5e**2)
		obja7mag = ina7mag[idx]+zpa7
		obja7me  = np.sqrt(ina7me[idx]**2 + zpa7e**2)

		print 'target magnitude \n'
		print 'auto mag and error', objatmag,objatme
		print 'ap3 mag and error', obja3mag,obja3me
		print 'ap5 mag and error', obja5mag,obja5me	
		print 'ap7 mag and error', obja7mag,obja7me

	except :
		objatmag,objatme = -99.,-99.
		obja3mag,obja3me = -99.,-99.
		obja5mag,obja5me = -99.,-99.
		obja7mag,obja7me = -99.,-99.
		

	#obja7mag.append((ina7mag[idx]+zpa7[i]))
	#obja7me.append((np.sqrt(ina7me[idx]**2 +zpa7e[i]**2)))

		print 'target magnitude \n'
		print 'auto mag and error', objatmag,objatme
		print 'ap3 mag and error', obja3mag,obja3me
		print 'ap5 mag and error', obja5mag,obja5me	
		print 'ap7 mag and error', obja7mag,obja7me

	return objatmag,objatme,zpat,zpate,obja3mag,obja3me,zpa3,zpa3e,obja5mag,obja5me,zpa5,zpa5e, obja7mag,obja7me, zpa7,zpa7e,len(index)

### photometry running 
def photrun(files) :
	refiles=files
	sedual(refiles)
	matchcom="stilts tskymatch2 ifmt1=csv ifmt2=ascii in1="+refcat+" in2=dual"+refiles[:-5]+".cat out=dual"+refiles[:-5]+".merge.cat ra1=radeg dec1=decdeg ra2=col4 dec2=col5 error=2 join=1and2 ofmt=ascii omode=out"
	os.system(matchcom)
	print 'Output catalog is : ','dual'+files[:-5]+'.merge.cat'	
	hdfiles='hd'+refiles
	sedual(hdfiles)
	print 'Output catalog is : ',hdfiles[:-5]+'.cat'	

### result phot file writing

k=open(outfile,'w')
tt=[]
k.write('# filename	obsdate	mjd	starnum	automag	automagerr	zpat	zpaterr	ap3mag	ap3magerr	zpa3	zpa3err	ap5mag	ap5magerr	zpa5	zpa5err	ap7mag	ap7magerr	zpa7	zpa7err\n')
for i in range(len(inlist)) :
	inimage = inlist[i]
	print str(i+1),' of ',len(inlist)
	head    = fits.getheader(inimage)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)
	photrun(inimage)
	magall=zpcal(inimage)
#	print tjd, stnum, obja3mag[i], obja3me[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
	#comment = str(tjd)+'\t'+str(list(snmag[i]))+'\t'+str(list(snmagerr[i]))+'\n'
	comment = inimage+'\t'+obsdate+'\t'+str(tjd)+'\t'+ str(magall[16])+'\t'+ \
              '%.3f' % magall[0]+'\t'+'%.3f' % magall[1]+'\t'+'%.3f' %magall[2]+'\t'+'%.3f' % magall[3]+'\t'+ \
              '%.3f' % magall[4]+'\t'+'%.3f' % magall[5]+'\t'+'%.3f' %magall[6]+'\t'+'%.3f' % magall[7]+'\t'+ \
              '%.3f' % magall[8]+'\t'+'%.3f' % magall[9]+'\t'+'%.3f' %magall[10]+'\t'+'%.3f' % magall[11]+'\t'+ \
              '%.3f' % magall[12]+'\t'+'%.3f' % magall[13]+'\t'+'%.3f' %magall[14]+'\t'+'%.3f' % magall[15]+'\t'+ \
              '\n'
	print comment	
	k.write(comment)
k.close()	
print '\a', 'Done, check result file...'





