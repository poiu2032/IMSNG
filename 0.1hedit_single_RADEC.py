from astropy.io import fits
from astropy.io import ascii
import os
import sys
import numpy as np
#from pyraf import iraf

# ============================== DESCRIPTION ===========================================
# Code for inserting header infomation automatically

# ============================== Source Code ==========================================

target_dir='/home/lim9/Desktop/IMSNG/9codes/alltarget.txt'
target=ascii.read(target_dir, Reader=ascii.NoHeader, guess=False)
obj = target['col1']
ra2 = target['col2']
dec2 = target['col3']

os.system('gethead ./acCal*.fits RA DEC')
os.system('ls acCal*.fits  > obj.list')
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
 	
for j in range(len(objlist)) :
 	data=fits.getdata(objlist[j])
	hdr=fits.getheader(objlist[j])

	print hdr['RA']
	print hdr['DEC']
 	
	if hdr['RA'] == "" and hdr['DEC'] == "" :
	
		objlist2=objlist[j]

		print 'Oh, '+str(objlist2)+' has no RA DEC...'
		print 'I will put these from alltarget.txt !'
 					
 		index = np.where(sys.argv[1] == obj)
		hdr.update(RA=ra2[index][0], DEC=dec2[index][0])
		fits.writeto(objlist[j], data, hdr, clobber=True)
		print str(objlist[j])+' done.'
		
os.system('gethead */acCal*.fits RA DEC')
print 'All done.'
 	
 	
 	
 	
 	
