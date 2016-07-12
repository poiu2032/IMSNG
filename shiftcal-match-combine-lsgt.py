# python code for shift calculation of serial images 
# Images are supposed to be shifted very little (a few arcse ~ a few arcmin) 
# 1. source detection of high signal/noise
# 2. set the first image to reference position
# 3. matching them to each other
# 4. calculate shift in pixel unit
# 5. image alignment based on shift 
# 6. image combination of shifted images 


import os
import sys
import numpy as np
import astropy.io.ascii as ascii
import matplotlib.pyplot as plt
import robust
import astropy.stats
from pyraf import iraf
import astropy.io.fits as fits

def imshift(im,dx,dy,out):
	iraf.imshift.unlearn()
	iraf.imshift.input=im
	iraf.imshift.output=out
	iraf.imshift.xshift=dx
	iraf.imshift.yshift=dy
	iraf.imshift.mode='h'
	iraf.imshift()

filename=sys.argv[1]
#os.system('ls cCalibrated*.fit > obj.list')
#infile='obj.list'
infile=filename
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

sextractor_dir='/home/sylee/Desktop/LOAO/Guideline_code/sex.config/'
shiftcalpar =sextractor_dir+'shiftcal.param'
shiftcalconf=sextractor_dir+'shiftcal.sex'

#source detection of high S/N = 10

for ll in lists :
	outcat=ll[:-4]+'cat'
	sextract_com='sex '+ll+' -c ' + shiftcalconf + \
				 ' -FILTER_NAME ' + sextractor_dir+'default.conv'+ \
				 ' -STARNNW_NAME '+ sextractor_dir+'default.nnw'+ \
				 ' -DETECT_THRESH 10' + ' -DETECT_MINAREA 10' + \
				 ' -CATALOG_NAME '+ outcat + ' -PARAMETERS_NAME '+shiftcalpar
	os.system(sextract_com)


# matching between two catalogs
#def match_shift(cat1,cat2,shift): 

#cat1=lists[0][:-4]+'.cat'
#cat2=lists[1][:-4]+'.cat'



#cat1dat=ascii.read(cat1)
#print len(cat1dat),'objects'
#cat2dat=ascii.read(cat2)
#print len(cat2dat),'objects'

def shiftcal(cat1,cat2):
	cat1dat=ascii.read(cat1)
	print len(cat1dat),'objects'
	cat2dat=ascii.read(cat2)
	print len(cat2dat),'objects'
	#print 'mathcing ',cat1,cat2

	dx,dy,dmag =[],[],[]

	for idx in range(len(cat1dat['NUMBER'])) :
		dist= np.sqrt( (cat1dat['X_IMAGE'][idx]-cat2dat['X_IMAGE'])**2 + (cat1dat['Y_IMAGE'][idx]-cat2dat['Y_IMAGE'])**2 )
		#print dist
		mindist=np.where(dist == np.min(dist))
		#print idx,' of Catalog 1'
		#print dist[mindist]
		#print (cat1dat['X_IMAGE'][idx]-cat2dat['X_IMAGE'][mindist]),  (cat1dat['Y_IMAGE'][idx]-cat2dat['Y_IMAGE'][mindist])
		dx.append((cat1dat['X_IMAGE'][idx]-cat2dat['X_IMAGE'][mindist])[0])
		dy.append((cat1dat['Y_IMAGE'][idx]-cat2dat['Y_IMAGE'][mindist])[0])
		dmag.append((cat1dat['MAG_AUTO'][idx]-cat2dat['MAG_AUTO'][mindist])[0])

	mx,stdx=robust.mean(dx,Cut=3.0)
	my,stdy=robust.mean(dy,Cut=3.0)
	mmag,stdmag=robust.mean(dmag,Cut=3.0)

	print 'x-shift',mx#, stdx
	print 'y-shift',my#, stdy
	#print 'mag-shift',mmag, stdmag
	return mx,my


os.system('cp '+lists[0]+' s'+lists[0])

outfiles=[]

cat0=lists[0][:-4]+'cat'

for ll in lists[1:] : 
	#d1=fits.getdata(lists[0])
	#d2=fits.getdata(ll)
	print ll
	llcat=ll[:-4]+'cat'
	dx1,dy1=shiftcal(cat0,llcat)
	print dx1,dy1
	imshift(ll,dx1,dy1,'s'+ll)
	outfiles.append('s'+ll)

outfiles.append('s'+lists[0])
group_before=(" ".join(lists))
group_after=(" ".join(outfiles))
os.system('ds9 -zscale '+ group_before +' -single -zoom to fit -match frame image &')	
os.system('ds9 -zscale '+ group_after +' -single -zoom to fit -match frame image &')	


