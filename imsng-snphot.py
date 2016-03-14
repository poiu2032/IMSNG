'''
This code is for differential photometry of SN object from images of IMSNG (LSGT, Maidanak, LOAO, SOAO)
Changsu Choi 2015/11/12

brief processes

#1. 	source extractor or daophot photometry of input image
#1.1 	dual mode? aperture? detect threshold? gain? other parameters?
#2. 	photometry of subtracted image : calculate SN object flux
#2.1	subtracted image check : astrometry tweak? or background anormality?

#3. 	calculate zero point from check stars : average of (check star mag(APASS) - instrument mag)  
#4. 	error : photometry error & zp error 
#5. 	check star mag check ensenble average
#6. 	adjust ap to SN object
'''

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
from astropy.coordinates import ICRS,SkyCoord

import robust
import string
import math
import pylab as pl
import glob
from PIL import Image
from matplotlib import pyplot as mpl
import subprocess
import aplpy

outfile='phot-result.dat'
inim='reahacCalibrated-MAIDANAK-NGC0337-20140920-213204-B-60.fits'
os.system('ls reahacCal*.fits > obj.list')
inlist = np.genfromtxt('obj.list',usecols=(0),dtype=str)
inlist = list(inlist)

detim='detection.fits'
filnames=['B','V','R']
apassfilnames=['Johnson_V','Verr','Johnson_B','B_err','convert_R', 'convert_Rerr']
os.system('cp /data0/code/sex.config/snphot* .' )
observatory=['LSGT','LOAO','Maidanak']
pixscales=[0.4815,0.7958,0.2679] # arcsec/pixel
aper3=[6.23,3.77,11.20]


# location of target in deg, single target!!
locx = 14.949292
locy = -7.5718333

# check star
cstar=ascii.read('../../cstar.cat')
radeg, raerr, decdeg, decerr, number_of_Obs=cstar['radeg'],cstar['raerr'],cstar['decdeg'], cstar['decerr'], cstar['number_of_Obs']
Johnson_V, Verr, Johnson_B, B_err=cstar['Johnson_V'], cstar['Verr'], cstar['Johnson_B'], cstar['B_err']
Sloan_g, gerr, Sloan_r, r_err, Sloan_i, i_err=cstar['Sloan_g'], cstar['gerr'], cstar['Sloan_r'], cstar['r_err'], cstar['Sloan_i'], cstar['i_err']
convert_R, convert_Rerr = cstar['convert_R'], cstar['convert_Rerr']


def sexcom(inim) : 
	print 'Souce Extractror is running on', inim
	detecthred   = '2'        ## sextractor parameter first for LSGT
	analthred    = '2'
	seeing       = '1.5'
	apersize     = '10,12,15'  # 3", 5", 7" aperture 0.2679"/pix
	detect='detection.fits'	  ## detection.fits is fine image show target significantly and have good seeing and many stars in it.
	secom='sex -c snphot.sex '+inim+' -CATALOG_NAME '+inim[:-5]+'.cat -SEEING_FWHM '+seeing+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred +' -PHOT_APERTURES '+apersize 
	os.system(secom)
	print 'Output catalog is : ',inim[:-5]+'.cat'

# output catalog
def zpcal(inim) : 
	incat=ascii.read(inim[:-5]+'.cat')
	cat1_ra=incat['ALPHA_J2000']
	cat1_dec=incat['DELTA_J2000']
	flag=incat['FLAGS']
	
	cat1_ra=incat['ALPHA_J2000']
	cat1_dec=incat['DELTA_J2000']
	flag=incat['FLAGS']

	cat2_ra=radeg
	cat2_dec=decdeg

	cat1 = SkyCoord(cat1_ra*u.degree,cat1_dec*u.degree,frame='icrs')
	cat2 = SkyCoord(cat2_ra*u.degree,cat2_dec*u.degree,frame='icrs')
	#index,dist2d,dist3d = cat1.match_to_catalog_sky(cat2,nthneighbor=1)
	index,dist2d,dist3d = cat2.match_to_catalog_sky(cat1)
	for i,j in enumerate(index):
		print cat2[i], "matches with ", cat1[j], "with a separation of ",dist2d[i]
		print cat2[1].to_string(precision=1, sep=':')

	apassmag=[]
	apassmage=[]
	instmag=[]
	instmage=[]
	zptmp=[]
	zpetmp=[]
	flagtmp=[]
	for k in range(len(index)) :	
		apassmag.append(Johnson_B[k])
		apassmage.append(B_err[k])
		instmag.append(incat['MAG_AUTO'][index[k]])
		instmage.append(incat['MAGERR_APER'][index[k]])
		zptmp.append(Johnson_B[k] - incat['MAG_APER'][index[k]])
		zpetmp.append(np.sqrt(B_err[k]**2 + incat['MAGERR_APER'][index[k]]**2))
		flagtmp.append(incat['FLAGS'][index[k]])

	print 'zero point values',zptmp
	print 'zero point errors',zpetmp
	print 'flag values', flagtmp
	print 'APASS magnitudes', apassmag
	print 'Instrument magnitudes', instmag

	zp=np.mean(zptmp)
	zpesum=0
	for zpe in zpetmp : 
		zpesum=zpe**2+zpesum
	zpe=np.sqrt(zpesum/len(zpetmp))
	postmag=zp+instmag
	magdiff=apassmag-postmag
	print 'zp= ', zp, 'zp err= ',zpe
	return zp,zpe,magdiff





def subphot(inim) :
	subim='hd'+inim
	sexcom(subim)
	subcat=ascii.read(subim[:-5]+'.cat')
	sra=subcat['ALPHA_J2000']
	sdec=subcat['DELTA_J2000']
	dist=np.sqrt((sra-locx)**2+ (sdec-locy)**2)
	snid=np.where(dist==min(dist))
	snid=snid[0][0]

	sninstmag=subcat['MAG_APER'][snid]
	sninstmage=subcat['MAGERR_APER'][snid]

	snmag=sninstmag + zp
	snmage=np.sqrt(sninstmage**2 + zpe**2)

	print 'SN mag',snmag, 'SN mag err', snmage
	return snmag, snmage

'''
sexcom(inim)
zp,zpe=zpcal(inim)
snmag,snmage=subphot(inim)
'''
tt=[]
k=open(outfile,'w')
k.write('# filename	dateobs	MJD	zp	zperr	SNmag	SNmagerr	magdiff1	magdiff2	magdiff3	magdiff4\n')

#k.write('# filename	dateobs	MJD	zp	zperr	SNmag	SNmagerr	magdiff1	magdiff2	magdiff3	magdiff4	magdiff5	magdiff6\n')

for i in range(len(inlist)) :
	inim=inlist[i] 
	print str(i+1),' of ',len(inlist)
	head    = fits.getheader(inim)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)

	sexcom(inim)
	zp,zpe,magdiff=zpcal(inim)
	snmag,snmage=subphot(inim)
	comment=inim+'\t'+obsdate+'\t'+str(tjd)+'\t'+'%.3f' % zp+ '\t'+'%.3f' % zpe + '\t'+'%.3f' % snmag +'\t'+'%.3f' % snmage+'\t'+'%.3f' % magdiff[0]+'\t'+'%.3f' % magdiff[1]+'\t'+'%.3f' % magdiff[2]+'\t'+'%.3f' % magdiff[3]+'\n'

#	comment=inim+'\t'+obsdate+'\t'+str(tjd)+'\t'+'%.3f' % zp+ '\t'+'%.3f' % zpe + '\t'+'%.3f' % snmag +'\t'+'%.3f' % snmage+'\t'+'%.3f' % magdiff[0]+'\t'+'%.3f' % magdiff[1]+'\t'+'%.3f' % magdiff[2]+'\t'+'%.3f' % magdiff[3]+'\t'+'%.3f' % magdiff[4]+'\t'+'%.3f' % magdiff[5]+'\n'

	k.write(comment)
	print comment
k.close()



# plot
import matplotlib.pyplot as plt
cat=ascii.read(outfile)
uvotcat=ascii.read('../../uvot_b.dat')

magdiff=[]
for i in range(len(cat['magdiff1'])) :
	magdifftmp=(cat['magdiff1'][i]+cat['magdiff2'][i]+cat['magdiff3'][i]+cat['magdiff4'][i])/4
	magdiff.append(magdifftmp)


fig = plt.figure()
ax = fig.add_subplot(111)


ax.scatter(tt,cat['SNmag'], marker='o',color='black',s=10)
ax.scatter(tt,cat['SNmag'] + magdiff, marker='o',color='blue',s=20)
ax.scatter(uvotcat['MJD[days]'],uvotcat['Mag'],marker='o',color='r',s=5)
ax.scatter(tt,cat['magdiff1']+20, marker='+',s=10,color='green')
ax.scatter(tt,cat['magdiff2']+21, marker='+',s=15,color='orange')
ax.scatter(tt,cat['magdiff3']+22, marker='+',s=20,color='yellow')
ax.scatter(tt,cat['magdiff4']+23, marker='+',s=25,color='cyan')

ax.set_ylim(25,10)
ax.set_xlim(56880,56980)
ax.set_title('Light curve of SN2014cx in B band')
ax.set_xlabel('MJD')
ax.set_ylabel('MAG (APASS catalog calibrated)')

ax.grid(True)

fig.savefig("lc_B.pdf")


print 'Done'
print '\a'


