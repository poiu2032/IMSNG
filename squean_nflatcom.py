# normalized flat combination code for squean data
# prepare bias-corrected flat images
# check flat images one by one, and if they are dome flat or skyflat
# If they have significant patterns on it, remove them from the list.

# usage example : squean_nflatcom.py Rflat.list Rflat.fits
#then it will give nRflat.fits to you.

import astropy.io.fits as fits
import numpy as np
from pyraf import iraf
from iraf import imred, ccdred
import os 
import sys

listname = sys.argv[1]
outfile = sys.argv[2]

os.system('rm '+outfile)
os.system('rm n'+outfile)

print "From the list of \'",listname, "\' combined dark image \' ",outfile, "\' will be produced" 

files=np.genfromtxt(listname,usecols=(0),dtype=str)
lists=list(files)

def flatcombine(lists,outname):
	iraf.unlearn(imred.flatcombine)
	group=(",".join(lists))
	ccdred.instrument = "ccddb$kpno/camera.dat"
	imred.flatcombine.combine = "median"
	imred.flatcombine.reject = "minmax"
	imred.flatcombine.ccdtype = ""
	imred.flatcombine.scale = "exposure"
	imred.flatcombine.process = "no"
#	imred.flatcombine.clobber = "yes"
	imred.flatcombine(group, output=outname)
#	iraf.imcombine.setParam('input',group)
#	iraf.imcombine.setParam('output',output)
#	iraf.imcombine.setParam('combine','median')
#	iraf.imcombine.setParam('combine',combine)
#	iraf.imcombine.setParam('combine','average')
#	iraf.imcombine.setParam('reject','none')
#	iraf.imcombine.setParam('zero','mode')
#	iraf.imcombine(group,output=output)

def imarith_divide(oper1,oper,oper2,outim) :
	iraf.unlearn(iraf.imarith)
	iraf.imarith.operand1=oper1
	iraf.imarith.op=oper
	iraf.imarith.operand2=oper2
	iraf.imarith.result=outim
	iraf.imarith.mode='h'
	iraf.imarith(oper1,op=oper,result=outim)
	
for fname in lists : 
	print fname,'filter =',fits.getheader(fname)['FILTER'], 'exptime =',fits.getheader(fname)['EXPTIME'],'obstype and object',fits.getheader(fname)['OBSTYPE'],fits.getheader(fname)['OBJECT']

for fname in lists :
	print 'mean,std = ',  fname ,"%0.2f" % float(np.mean(fits.getdata(fname))),"%0.2f" % float(np.std(fits.getdata(fname)))



flatcombine(lists,outfile)


print 'mean,std value of ',outfile, "%0.2f" % float(np.mean(fits.getdata(outfile))), "%0.2f" % float(np.std(fits.getdata(outfile)))

imarith_divide(outfile,'/',float(np.mean(fits.getdata(fname))),'n'+outfile)
outfile='n'+outfile

print 'mean,std value of ',outfile, "%0.2f" % float(np.mean(fits.getdata(outfile))), "%0.2f" % float(np.std(fits.getdata(outfile)))



print "Done, check the image", "\a"



