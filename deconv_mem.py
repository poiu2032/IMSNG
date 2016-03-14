from astropy.io import ascii
import os
import sys
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
from astropy.time import Time
from astropy.io import ascii
from astropy.table import Table, Column
from astropy.io.votable import parse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import interpolate
from pyraf import iraf
from pyraf.iraf import stsdas
os.system('rm mem*.fits')

inimage    = sys.argv[1]

def psfexxml(xmlfile):
	votable=parse(xmlfile)
	table=votable.get_first_table()
	data= table.array
	table=votable.get_first_table()
	data= table.array

	data['FWHM_Mean']
	fmp=data['FWHM_Mean'][0]
	#fmw=data['FWHM_WCS_Mean'][0] 
	#ps=data['PixelScale_WCS_Mean'][0]
	#em=data['Ellipticity_Mean'][0]

#	print "FWHM in pixel, ",fmp # , " FWHM in Arcsec, ",fmw, " pixel scale, ",ps
	return fmp


def imcopy(impsffile) :
	iraf.imutil.imcopy.setParam('input',impsffile+'[100:125,100:125]')
	iraf.imutil.imcopy.setParam('output','cut'+impsffile)
	iraf.imutil.imcopy(mode='h')


def mem(inimage,inpsf,output):
	iraf.stsdas.analysis.restore.mem.setParam('input',inimage)
	iraf.stsdas.analysis.restore.mem.setParam('psf',inpsf)
	iraf.stsdas.analysis.restore.mem.setParam('output',output)
	iraf.stsdas.analysis.restore.mem.setParam('maxiter',100)
	iraf.stsdas.analysis.restore.mem.setParam('noise',15)
	iraf.stsdas.analysis.restore.mem.setParam('adu',2.3)
#	iraf.mem.(inimage,inpsf,output,maxiter)
	iraf.stsdas.analysis.restore.mem(mode='h')

presecom="sex -c prepsfex.sex "+inimage+" -CATALOG_NAME "+inimage[:-5]+".cat"
psfexcom="psfex -c default.psfex "+inimage[:-5]+".cat"
os.system(presecom)
os.system(psfexcom)
os.system('cp psfex.xml '+inimage[:-5]+'.xml')	
psfexxml(inimage[:-5]+'.xml')
print inimage, ' fwhm value is ', psfexxml(inimage[:-5]+'.xml')

inpsffile='snap_'+inimage


output='mem'+inimage

imcopy(inpsffile)

inpsf='cut'+inpsffile

mem(inimage,inpsf,output)



os.system("cp /data0/code/psfex.config/* .")

presecom="sex -c prepsfex.sex "+output+" -CATALOG_NAME "+output[:-5]+".cat"
psfexcom="psfex -c default.psfex "+output[:-5]+".cat"
os.system(presecom)
os.system(psfexcom)
os.system('cp psfex.xml '+output[:-5]+'.xml')	
psfexxml(output[:-5]+'.xml')
print output, ' fwhm value is ', psfexxml(output[:-5]+'.xml')


