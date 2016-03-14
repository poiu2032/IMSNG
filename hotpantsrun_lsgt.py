from astropy.io import ascii
import numpy as np
import os
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u


os.system('ls recCal*.fits > obj.list')

os.system('rm hdrecCal*.fits')
os.system('rm hcrecCal*.fits')

objfile='obj.list'
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
infile=objlist

for n in range(len(infile)):
	outfile='hd'+infile[n]
	convfile='hc'+infile[n]
	com='hotpants -v 0 -inim '+infile[n]+' -tmplim ref.fits -outim '+outfile+' -oci '+convfile
	#com='hotpants -v 0 -c i -n i -inim '+infile[n]+' -tmplim ref.fits -outim '+outfile+' -oci '+convfile
	print n, 'of ',len(infile),infile[n]
	print '\n\n\n\n'
	os.system(com)

print 'all done, check it out!'
print '\a'
#os.system('ds9 hdrecCal*.fits &')
