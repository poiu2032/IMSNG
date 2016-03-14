#astrometry.net script making program for ONE target
#output file is "astrometry_current_dir.sh"
#
from astropy.io import ascii
import numpy as np
import os
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u

#making default.sex file for using sextractor option 
os.system('sex -d > default.sex')
#making list file  ' obj.list ' for *.fit
#you can change other option for 'ls' parameter : this is for itelescope Calibrated data
os.system('ls *.fit > obj.list')
objfile='obj.list'
#objlist=ascii.read(objfile,guess=False,NoHeader)
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)

olist = objlist


#ra='09:37:01'
#dec='+01:05:43.00'
addlist=[]
for n in range(len(olist)):
	print olist[n]
	addlist.append(olist[n])

command=[]

f=open("astrometry_current_dir.sh",'w')
n=0
for n in range(len(olist)):
	header=fits.getheader(olist[n])	
	ra=header['ra']
	dec=header['dec']
	rad=coord.Angle(ra,unit=u.hour)	
	radd=rad.degree
	decd=coord.Angle(dec,unit=u.deg)
	decdd=decd.degree	
	com='solve-field '+addlist[n]+' --scale-unit arcsecperpix --scale-low 0.3 --scale-high 0.9 --ra '+str(radd)+' --dec '+str(decdd)+', --radius 0.5 --no-plots --new-fits '+addlist[n]+'s --overwrite --use-sextractor\n'
	f.write(com)


f.close()

# run the script for astrometry
# check /tmp with 'df -h' command whether it is full or not; it should have enough space

os.system('sh astrometry_current_dir.sh')
