## refine astrometry with scamp
## need already astrometry-done files with astrometry.net
## need reference catalog from reference image's astrometry with scamp : option "save reference = yes" 
#python scampastrom.py obj.list

from astropy.io import ascii
import numpy as np
import os,sys
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import subprocess


subprocess.call('ls acCalibrate*.fits > obj.list',shell=True)
objfile='obj.list'
os.system('cp /data0/code/astrom/astrom.* .')
os.system('cp /data0/code/psfex.config/* .')
#objfile=sys.argv[1]

#os.system('rm ahcC*.fits')
os.system('rm sreacC*.fits')
#resnum=subprocess.check_output('ls cCalibrate*.fits | wc -l',shell=True)
#print "files pre-astrometry done : ", resnum
objlist=np.genfromtxt(objfile,usecols=(0),dtype=str)


#refcat='/data0/itelescope_data/t52/NGC2442/com/USNO-B1.0_0736-6932_r12.cat'

dolist=[]
nolist=[]
os.system('rm tmp.fits')
def scamp(files) :
	#prehead  = fits.getheader(files[1:-1])	
	#prehead  = fits.getheader(files)	
	sexcom  = 'sex -c astrom.sex '+files+' -catalog_name '+files[:-5]+'.cat'  
	#scampcom = 'scamp -c astrom.scamp '+files[:-5]+'.cat -ASTREF_CATALOG FILE -CHECKPLOT_DEV NULL -ASTREFCAT_NAME '+refcat
	scampcom = 'scamp -c astrom.scamp '+files[:-5]+'.cat -ASTREF_CATALOG 2MASS -CHECKPLOT_DEV NULL' #-ASTREFCAT_NAME '+refcat

	#presecom = "sex -c prepsfex.sex "+files+" -CATALOG_NAME "+files[:-5]+".cat"
	#psfexcom = "psfex -c default.psfex "+files[:-5]+".cat"
	swarpcom = 'swarp -c astrom.swarp '+files+' -IMAGEOUT_NAME ah'+files+' -COPY_KEYWORDS OBJECT,DATE-OBS,EXPTIME,FILTER,RA,DEC,AIRMASS,OBSERVAT,JD' #-CENTER_TYPE MANUAL -CENTER 07:36:21.905,-69:32:01.26' # -IMAGE_SIZE 2400,1600

	#os.system(presecom)
	#os.system(psfexcom)

	os.system(sexcom)
	tmpcatname=files[:-5]+'.cat'
	os.system('ldactoasc '+tmpcatname+' > tmp.cat')
	tmpcat=ascii.read('tmp.cat')

	if max(tmpcat['NUMBER']) < 10 : 
		print 'I will not touch this, it has stars less than 10. \n'
		nolist.append(files)
	else :
		print 'Scamp will do this!! \n'
		os.system(scampcom)
		os.system(swarpcom)
		#posthead = fits.getheader('s'+files)
		#hdu      = fits.getdata('s'+files)
		#finalhead= prehead+posthead
		#fits.writeto('rah'+files,hdu,finalhead,clobber=True)
		dolist.append(files)

for i in range(len(objlist)) :	
	scamp(objlist[i]) 
	print i,' th of ', len(objlist)
print 'all done ',len(dolist),'from ',len(objlist),' files' 
print nolist
print '\a'

g=open('scampastrom_log.txt','w')
g.write('# do list \n')

for n in range(len(dolist)) :
	g.write(dolist[n]+'\n')

g.write('# no list : less than 10 stars on image \n')

for m in range(len(nolist)) :
	g.write(nolist[m]+'\n')

g.close()


	
