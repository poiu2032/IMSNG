from astropy.io import ascii
import numpy as np
import os,sys
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import subprocess

subprocess.call('ls cCT*.fit > obj.list',shell=True)
os.system('sex -d > default.sex')
objfile='obj.list'
#colnames=('direc','obsdate','fname')
colnames=('fname')
#objlist=ascii.read(objfile,names=colnames,Reader=ascii.NoHeader,guess=False,delimiter='/')
objlist=ascii.read(objfile,Reader=ascii.NoHeader,guess=False)
addlist=objlist['col1']

#ra='09:37:01'
#dec='+01:05:43.00'
#addlist=[]
#for j in range(len(objlist)):
#	olist = objlist['direc'][j]+'/'+str(objlist['obsdate'][j])+'/'+objlist['fname'][j]
#	print olist
#	addlist.append(olist)

command=[]

f=open("astrometry_current_dir.sh",'w')
n=0
for n in range(len(addlist)):
	header=fits.getheader(addlist[n])	
	print addlist[n]
	ra=header['RA']
	dec=header['DEC']
	rad=coord.Angle(ra,unit=u.hour)	
	radd=rad.degree
	decd=coord.Angle(dec,unit=u.deg)
	decdd=decd.degree	
	com='solve-field \''+addlist[n]+'\' --scale-unit arcsecperpix --scale-low 0.4 --scale-high 0.8 --ra '+str(radd)+' --dec '+str(decdd)+', --radius 0.7 --no-plots --new-fits \'a'+addlist[n]+'s\' --overwrite --use-sextractor --temp-dir .\n'
	print com
	f.write(com)


f.close()

subprocess.call('sh astrometry_current_dir.sh',shell=True)
subprocess.call('ls c*.fits > obj.list.done',shell=True)

orinum=subprocess.check_output('ls c*.fit | wc -l',shell=True)

resnum=subprocess.check_output('ls c*.fits | wc -l',shell=True)

print "from ",orinum[:-1],"files , ",resnum[:-1] ,"files are solved"
print "all done"

os.system('rm tmp*')
