#psfexrun.py
#usage : python psfexrun.py imagelist

import os,sys
import numpy as np
from astropy.io import ascii
from astropy.io import fits
from astropy.time import Time
from astropy.io.votable import parse
from astropy.time import Time
import robust
import matplotlib.pyplot as plt

infile= sys.argv[1]
inlist= np.genfromtxt(infile,usecols=(0),dtype=str)
inlist=list(inlist)
os.system("cp /home/sylee/Desktop/LOAO/Guideline_code/psfex.config/* .")

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

for inimage in inlist :

	presecom="/usr/bin/sex -c prepsfex.sex "+inimage+" -CATALOG_NAME "+inimage[:-5]+".cat"
	psfexcom="/usr/bin/psfex -c default.psfex "+inimage[:-5]+".cat"
	os.system(presecom)
	os.system(psfexcom)
	os.system('cp psfex.xml '+inimage[:-5]+'.xml')	
	psfexxml(inimage[:-5]+'.xml')
#	print inimage, ' fwhm value is ', psfexxml(inimage[:-5]+'.xml')
	os.system('imcopy snap_'+inimage+'[100:125,100:125] psf'+inimage)

#print 'all done'

