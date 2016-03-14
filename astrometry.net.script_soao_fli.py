from astropy.io import ascii
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord

import os
import sys
import numpy as np
import subprocess

targets=ascii.read('/data0/SOAO/alltarget.txt')
os.system('ls cCalibrated*.fits > obj.list')
os.system('sex -d > default.sex')
#os.system('cp /')
objfile='obj.list'
objlist=ascii.read(objfile,Reader=ascii.NoHeader,guess=False)
addlist=objlist['col1']

command=[]

#f=open("astrometry_current_dir.sh",'w')

n=0
for n in range(len(addlist)):
	#header=fits.getheader(addlist[n])	
	#ra=header['ra']
	#dec=header['dec']
	ra=targets['ra'][targets['obj']==addlist[n][17:-26]][0]
	dec=targets['dec'][targets['obj']==addlist[n][17:-26]][0]
	rad=coord.Angle(ra,unit=u.hour)	
	radd=rad.degree
	decd=coord.Angle(dec,unit=u.deg)
	decdd=decd.degree	
	#com='solve-field \''+addlist[n]+'\' --scale-unit arcsecperpix --scale-low 0.3 --scale-high 0.9 --ra '+str(radd)+' --dec '+str(decdd)+', --radius 0.5 --no-plots --new-fits '+'a'+addlist[n]+' --overwrite --use-sextractor\n'
	com='solve-field \''+addlist[n]+'\' --scale-unit arcsecperpix --scale-low 0.3 --scale-high 0.9 --ra '+str(radd)+' --dec '+str(decdd)+', --radius 0.5 --no-plots --new-fits '+'a'+addlist[n]+' --overwrite \n' #--use-sextractor\n'

	print n, ' ,th file of ',len(addlist),'\n\n'
	print com,'\n'
	os.system(com)

#	f.write(com)


#f.close()

#subprocess.call('sh astrometry_current_dir.sh',shell=True)
os.system('ls acCalibrated*.fits > obj.list.done') # ,shell=True)

orinum=subprocess.check_output('ls cCalibrated*.fits | wc -l',shell=True)
resnum=subprocess.check_output('ls acCalibrated*.fits | wc -l',shell=True)

print "from ",orinum[:-1],"files , ",resnum[:-1] ,"files are solved"
print "all done"
print '\a'

