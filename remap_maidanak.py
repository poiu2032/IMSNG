#wcs remapping of input image to reference image using wcstools remap or wcsremap(Andrew Becker)
#obj.list file is necessary
#astrometry must be done before doing this!! -- scampastrom.py


from astropy.io import ascii
import numpy as np
import os,sys
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import subprocess

os.system('rm reahacCal*.fits')
#subprocess.call('ls cCalibrate*.fits > obj.list',shell=True)
os.system('ls ahacCal*.fits > obj.list')
objfile='obj.list'
objlist=np.genfromtxt(objfile,usecols=(0),dtype=str)

ref='ref.fits'
pixscale=0.2677

for files in objlist :
	print str(list(objlist).index(files)+1),'of ',str(len(objlist)+1),' files'
	
	#'wcsremap' : andrew becker
	#remapcom = 'wcsremap -template ref.fits -source '+files+' -outIm re'+files          
	#'remap' of wcstools : head infomation will be copied to input image, to be corrected soon 2015/05/04
	remapcom='remap -v -f ref.fits '+' -p '+str(pixscale)+' -o re'+files+' '+files
	#print remapcom
	os.system(remapcom)
	# header editting to propagete keywords from original files
	inheader=fits.getheader(files)
	output='re'+files
	outdata,outheader=fits.getdata(output, header=True)
	outheader['UTSTART'] = inheader['UTSTART']
	outheader['UTDATE'] = inheader['UTDATE']	
	outheader['DATE-OBS']= inheader['UTDATE']+'T'+inheader['UTSTART']
	outheader['OBJECT']   = inheader['OBJECT']
	#outheader['TELESCOP'] = inheader['TELESCOP']
	fits.writeto(output, outdata, outheader, clobber=True)

print 'all done '+str(len(objlist))+' files'
os.system('ds9 re*.fits &')
