# bias combination code for squean data
# usage : squean_biascom.py bias.list zero.fits

import astropy.io.fits as fits
import numpy as np
from pyraf import iraf
from iraf import imred, ccdred
import os 
import sys

listname = sys.argv[1]
outfile = sys.argv[2]

os.system('rm '+outfile)

print "From the list of \'",listname, "\' combined bias image \' ",outfile, "\' will be produced" 

files=np.genfromtxt(listname,usecols=(0),dtype=str)
lists=list(files)

def zerocombine(lists,outname):
	group=(",".join(lists))
	iraf.unlearn(imred.zerocombine)
	ccdred.instrument = "ccddb$kpno/camera.dat"
	imred.zerocombine.combine = "median"
	imred.zerocombine.reject = "minmax"
	imred.zerocombine.ccdtype = ""
	imred.zerocombine.scale = "none"
	imred.zerocombine(group, output=outname)
#	iraf.imcombine.setParam('input',group)
#	iraf.imcombine.setParam('output',output)
#	iraf.imcombine.setParam('combine','median')
#	iraf.imcombine.setParam('combine',combine)
#	iraf.imcombine.setParam('combine','average')
#	iraf.imcombine.setParam('reject','none')
#	iraf.imcombine.setParam('zero','mode')
#	iraf.imcombine(group,output=output)

for fname in lists :
	print 'mean,std = ',  fname ,"%0.2f" % float(np.mean(fits.getdata(fname))),"%0.2f" % float(np.std(fits.getdata(fname)))

print "Done, check the image", "\a"

zerocombine(lists,outfile)
print 'mean,std value of ',outfile, "%0.2f" % float(np.mean(fits.getdata(outfile))), "%0.2f" % float(np.std(fits.getdata(outfile)))







