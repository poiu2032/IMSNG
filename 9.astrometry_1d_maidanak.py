#astrometry.net script making program for ONE target

from astropy.io import ascii
from astropy.io import fits
import numpy as np
import os
import sys
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import subprocess

os.system('ls -d m* ngc* M* NGC* messier* IC* CGC* ic* ugc* UGC* PGC*  IRAS* > direc.list')
alllist=np.genfromtxt('direc.list',usecols=(0),dtype=str)
for i in range(len(alllist)) :
	os.chdir(alllist[i])

	subprocess.call('ls cCal*.fits > astrom.list',shell=True)

	os.system('sex -d > default.sex')
	objfile='astrom.list'
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
#command=[]

	f=open("./astrometry_current_dir.sh",'w')
	n=0
	for n in range(len(addlist)):
		header=fits.getheader(addlist[n])	
		ra=header['ra']
		dec=header['dec']
		
		if ra == '00:00:00.000' and dec == '+00:00:00.00' :
			# Read alltarget.txt and load ra dec of corresponding target.
			print 'Oh, RA & DEC are not in their Header...'
			print 'I will bring these from alltarget.txt !'
			target_dir='/home/lim9/Desktop/IMSNG/9codes/alltarget.txt'
			target=ascii.read(target_dir, Reader=ascii.NoHeader, guess=False)
			obj = target['col1']
			ra2 = target['col2']
			dec2 = target['col3']

			if alllist[i] in obj : 
				index = np.where(alllist[i] == obj)
				ra=ra2[index]
				dec=dec2[index]
		
		rad=coord.Angle(ra,unit=u.hour)	
		radd=rad.degree
		decd=coord.Angle(dec,unit=u.deg)
		decdd=decd.degree	
		com='solve-field \''+addlist[n]+'\' --temp-dir /run/media/lim9/data2/preprocessing/temp --scale-unit arcsecperpix --scale-low 0.1 --scale-high 0.7 --ra '+str(radd[0])+' --dec '+str(decdd[0])+', --radius 0.5 --no-plots --new-fits a'+addlist[n]+' --overwrite --use-sextractor\n'
		
		else :
			rad=coord.Angle(ra,unit=u.hour)	
			radd=rad.degree
			decd=coord.Angle(dec,unit=u.deg)
			decdd=decd.degree	
			com='solve-field \''+addlist[n]+'\' --temp-dir /run/media/lim9/data2/preprocessing/temp --scale-unit arcsecperpix --scale-low 0.1 --scale-high 0.7 --ra '+str(radd)+' --dec '+str(decdd)+', --radius 0.5 --no-plots --new-fits a'+addlist[n]+' --overwrite --use-sextractor\n'
		
		
		
		print com
		f.write(com)

	f.close()
	subprocess.call('sh astrometry_current_dir.sh', shell=True)

	orinum=subprocess.check_output('ls cCal*.fits | wc -l', shell=True)
	resnum=subprocess.check_output('ls acCal*.fits | wc -l', shell=True)

	print "From ",orinum[:-1],"files , ",resnum[:-1] ,"files are solved."
	os.chdir('../')
os.system('rm -r /run/media/lim9/data2/preprocessing/temp/*')
print "All done."
print 'All Preprocessing is finished !, After copying ref.fits, Run remap code !'

