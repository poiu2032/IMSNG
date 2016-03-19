
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

os.system('ls -d m* ngc* M* NGC* messier* IC* CGC* ic* ugc* UGC* PGC* IRAS* > direc.list')
alllist=np.genfromtxt('direc.list', usecols=(0),dtype=str)
os.system('gethead */acCal*.fits RA DEC')
for i in range(len(alllist)) :
 	os.chdir(alllist[i])
 	
 	os.system('ls acCal*.fits  > obj.list')
	objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
 	
 	for j in range(len(objlist)) :
	 	data=fits.getdata(objlist[j])
 		hdr=fits.getheader(objlist[j])
 		
 		#data=fits.open(objlist[j], mode='update')
 		print hdr['RA']
 		print hdr['DEC']
 	 		
 		if hdr['RA'] == '' and hdr['DEC'] == '' :
 			print 'Oh, '+str(objlist[j])+' has no RA DEC...'
 			print 'I will put these from alltarget.txt !'
 					
 		 	index = np.where(alllist[i] == obj)
 			hdr.update(RA=ra2[index][0], DEC=dec2[index][0])
 			fits.writeto(objlist[j], data, hdr, clobber=True)
		print str(objlist[j])+' done.'
		
 	os.chdir('../')
os.system('gethead */acCal*.fits RA DEC')
print 'All done.'
 	
 	
 	
 	
 	
