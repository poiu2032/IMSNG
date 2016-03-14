# make reference image from ref.list
# need ref.list

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

#os.system('rm ref.fits')

infile='ref.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
group=list(files)

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



def imcombine(group,output):
	group=(",".join(group))
#	combine=average
	iraf.imcombine.setParam('input',group)
	iraf.imcombine.setParam('output',output)
	iraf.imcombine.setParam('combine','median')
#	iraf.imcombine.setParam('combine',combine)
#	iraf.imcombine.setParam('combine','average')
	iraf.imcombine.setParam('reject','none')
	iraf.imcombine(group,output=output)

imcombine(group,'ref.fits')

group.append('ref.fits')
fwhm=[]
g=open('ref_fwhm.txt','w')
for i in range(len(group)) :
	files=group[i]
	presecom="sex -c prepsfex.sex "+files+" -CATALOG_NAME "+files[:-5]+".cat"
	psfexcom="psfex -c default.psfex "+files[:-5]+".cat"
	os.system(presecom)
	os.system(psfexcom)
	os.system('cp psfex.xml '+files[:-5]+'.xml')
	psfexxml(files[:-5]+'.xml')
	fwhm.append(psfexxml(files[:-5]+'.xml'))
	comment=group[i]+'\t'+str(psfexxml(files[:-5]+'.xml'))
	g.write(comment+'\n')
g.close()



for i in range(len(group)) :
	print group[i],fwhm[i]

print 'reference frame is ready, \'ref.fits\' fwhm value is ', fwhm[i]
print '\a'

