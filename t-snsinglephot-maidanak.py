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
from matplotlib import pyplot as plt
import subprocess
import aplpy


# location of target in deg, single target!!
locx = 14.949292
locy = -7.5718333
# SN2014cx

'''
14.969510,0.202,-7.684650,0.169,4,14.329,0.019,15.164,0.035,14.835,0.022,14.098,0.019,13.769,0.068,13.858,0.071
14.943198,0.260,-7.691065,0.267,5,14.434,0.027,15.271,0.038,14.948,0.021,14.125,0.014,13.778,0.063,13.879,0.065
14.861105,0.750,-7.640510,0.583,4,16.284,0.033,16.720,0.056,16.591,0.040,16.144,0.056,16.011,-0.000,15.961,0.056
14.855961,0.238,-7.607581,0.267,5,14.504,0.019,15.217,0.037,14.945,0.005,14.280,0.006,14.072,0.058,14.075,0.058
'''
#locx = 14.855961
#locy = -7.607581

'''
try : 
	glob.glob('detection.fits')
	print '\n Chech the location of target and other parameters'
except : 
	print '\n No detection.fits'
	print ' Make a detection.fits and run me again.' 
	sys.exit()
'''


objmag    = []
objmagerr = []

dirhere = os.getcwd()
dirhere = dirhere.split('/') 
outfile = dirhere[3]+'-'+dirhere[5]+'-phot_ch3.txt'    ##  'NGC0337-R-phota.txt'
refcat  = '../apass_NGC0337.cat'            ##  ex) ../apass_NGC0337.cat
#refcat  = '../../cstar.cat'

os.system('ls reacCal*.fits > obj.list')
inlist = np.genfromtxt('obj.list',usecols=(0),dtype=str)
inlist = list(inlist)

filters      = ['Johnson_B','Johnson_V','convert_R']
errors       = ['B_err','Verr','convert_Rerr']
filtershere  = ['B','V','R']
errname      = errors[filtershere.index(dirhere[5])]
filname      = filters[filtershere.index(dirhere[5])] 

## source extractor parameter
#os.system('cp /data0/code/sex.config/snphot* .' )
 # x pix scale 0.5

### sextractor dual mode, detection.fits is fine image shows target significantly and has good seeing and many stars in it.
def sedual(measure) : 
	print 'souce extractror is running on', measure
	detecthred   = '3'        ## sextractor parameter first for LSGT
	analthred    = '2'
	seeing       = '1.5'
	apersize     = '11,18.5,26'  # 3", 5", 7" aperture 0.2679"/pix
	detect='detection.fits'	  ## detection.fits is fine image show target significantly and have good seeing and many stars in it.
	sedualcom='sex -c snphot.sex '+measure+' -CATALOG_NAME '+measure[:-5]+'.cat -SEEING_FWHM '+seeing+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred +' -PHOT_APERTURES '+apersize 
	os.system(sedualcom)
	print 'Output catalog is : ',measure[:-5]+'.cat'
	


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
	mcat=im[:-5]+'.merge.cat'
	mcat=ascii.read(mcat)
	mmag=mcat['Johnson_B']
	#mmag=mcat['convert_R']	
	sra =mcat['col4'] 
	sdec=mcat['col5']
	stel=mcat['col15']
	flag=mcat['col14'] 
	atmag, atme = mcat['col6'], mcat['col7']  
	a3mag, a3me = mcat['col8'], mcat['col9'] 
	a5mag, a5me = mcat['col10'],mcat['col11']  
	a7mag, a7me = mcat['col12'],mcat['col13']

	outradius=10/60.	 ## arcmin unit
	inradius= 1/60.
	dist=np.sqrt((sra-locx)**2+ (sdec-locy)**2)
	index=np.where((dist > inradius) & (dist < outradius) & (atme < 0.2)  & (flag == 0) & (mmag > 12.5) & (mmag < 16.5))  ## inside ouradius and outside inradius, error < 0.2,   flag value < 5,  
	index=list(index[0])
	print len(index)
	
	refmag, refme = mcat[filname],mcat[errname]
	
	stnum=len(refmag)
	aval=robust.mean(refmag[index] - atmag[index] ,Cut=5.0)    #zp and error for one image
	zpat,zpate = aval[0],aval[1]
	#zpat.append(aval[0])
	#zpate.append(aval[1])	
	aval=robust.mean(refmag[index] - a3mag[index] ,Cut=5.0)    #zp and error for one image
	zpa3,zpa3e = aval[0],aval[1]
	#zpa3.append(aval[0])
	#zpa3e.append(aval[1])	
	
	aval=robust.mean(refmag[index] - a5mag[index] ,Cut=5.0)    #zp and error for one image
	zpa5,zpa5e = aval[0],aval[1]
	#zpa3.append(aval[0])
	#zpa3e.append(aval[1])	

	aval=robust.mean(refmag[index] - a7mag[index] ,Cut=5.0)    #zp and error for one image
	zpa7,zpa7e = aval[0],aval[1]
	#zpa3.append(aval[0])
	#zpa3e.append(aval[1])	

	# for each input image, calculate magnitude of target from hdrecCal~~.fits
	incat='hd'+im[:-5]+'.cat'
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

	fig = plt.figure()
	ax = fig.add_subplot(111)
	#ax.scatter(refmag[index],refmag[index]-a3mag[index], fmt='o',color='b',s=5)
	ax.hlines(zpa3,10,20,linestyles='dashed')
	ax.hlines(zpa5,10,20,linestyles='dashed')
	ax.hlines(26.5,10,20,linestyles='dashdot')
	ax.errorbar(refmag[index],refmag[index]-a3mag[index],yerr=a3me[index],fmt='o')
	ax.errorbar(refmag[index],refmag[index]-(zpa3+a3mag[index])+26.5,yerr=zpa3e,fmt='*')
	ax.errorbar(refmag[index],refmag[index]-a5mag[index],yerr=a5me[index],fmt='o')
	ax.errorbar(refmag[index],refmag[index]-(zpa5+a5mag[index])+25.5,yerr=zpa5e,fmt='*')

	for idx in index :		
		print 'mag',(zpa5+a5mag[idx]),'ra',sra[idx]

	#ax.set_xlim(,12000)
	#ax.set_ylim(2,4)
	ax.grid(True)
	ax.set_title('zeropoint '+im)
	ax.set_ylabel('APASS mag-instrument')
	ax.set_xlabel('APASS mag')
	ax.set_xlim(12,18)
	ax.set_ylim(25,29)
	leg=['ap 3','ap3 ref-phot+26.5','ap5','ap5 ref-phot+25.5']
	ax.legend(leg,loc='upper right', fontsize='medium')
	fig.savefig(im[:-5]+'.jpg')
	fig.clf()



	return objatmag,objatme,zpat,zpate,obja3mag,obja3me,zpa3,zpa3e,obja5mag,obja5me,zpa5,zpa5e, obja7mag,obja7me, zpa7,zpa7e,len(index)















### photometry running 
def photrun(files) :
	refiles=files
	sedual(refiles)
	matchcom="stilts tskymatch2 ifmt1=csv ifmt2=ascii in1="+refcat+" in2="+refiles[:-5]+".cat out="+refiles[:-5]+".merge.cat ra1=radeg dec1=decdeg ra2=col4 dec2=col5 error=1 join=1and2 ofmt=ascii omode=out"
	os.system(matchcom)
	print 'Output catalog is : ',files[:-5]+'.merge.cat'	
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
'''
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
fig.clf()

print 'Done'
print '\a'
'''

print '\a', 'Done, check result file...'





