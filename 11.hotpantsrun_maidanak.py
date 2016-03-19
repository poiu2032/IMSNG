from astropy.io import ascii
import numpy as np
import os
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u


os.system('ls reacC*.fits > obj.list')

#os.system('rm hd*.fits')
#os.system('rm hc*.fits')

objfile='obj.list'
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
infile=objlist

for n in range(len(infile)):
	outfile='hd'+infile[n]
	convfile='hc'+infile[n]
	com='hotpants -v 0 -inim '+infile[n]+' -tmplim ref2.fits -outim '+outfile+' -oci '+convfile+' -iu 50000 '
	#com='hotpants -v 0 -c i -n i -inim '+infile[n]+' -tmplim ref.fits -outim '+outfile+' -oci '+convfile
	print infile[n]
	os.system(com)

print 'all done, check it out!'
os.system('python /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/12.detect_maidanak.py')