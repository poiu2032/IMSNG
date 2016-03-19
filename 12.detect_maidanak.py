import os
import sys
import numpy as np
from astropy.io import fits
from astropy.io import ascii
from astropy.time import Time
import astropy.units as u
import astropy.coordinates as coord
from astropy.io.votable import parse
from astropy.table import Table, Column
import string
import math
import pylab as pl
import glob
from PIL import Image
from matplotlib import pyplot as mpl
import subprocess
import aplpy

os.system('ls acCal*.xml > xml.list')
xmlfile= np.genfromtxt('xml.list', usecols=(0), dtype=str)

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



# reading list file of subtracted images
os.system('ls hd*.fits > subobj.list')
inlist= np.genfromtxt('subobj.list',usecols=(0),dtype=str)
inlist=list(inlist)

# running sextractor for subtracted image

detecthred = '5'
analthred  = '3'
apersize='3,5,7,9,11,13,15,17,19,21'

def sex(inimage) :
	tmpimage=inimage[4:]
#	presecom="sex -c prepsfex.sex "+inimage+" -CATALOG_NAME "+inimage[:-5]+".cat"
#	psfexcom="psfex -c default.psfex "+inimage[:-5]+".cat"
#	os.system(presecom)
#	os.system(psfexcom)	
#	os.system('cp psfex.xml '+inimage[:-5]+'.xml')	
	psfexxml(tmpimage[:-5]+'.xml')	
#	fwhm.append(psfexxml(tmpimage[:-5]+'.xml'))
	sexcom='sex -c phot.sex '+inimage+' -CATALOG_NAME '+inimage[:-5]+'.cat -PARAMETERS_NAME  phot.param -psf_name '+tmpimage[:-5]+'.psf -seeing_fwhm '+str(psfexxml(tmpimage[:-5]+'.xml'))+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred+' -PHOT_APERTURES '+apersize 
	os.system(sexcom)


for images in inlist :
	sex(images)


# make stamp
#subcat=ascii.read(inimage[:-5]+'.cat')
#ra=subcat['ALPHA_J2000']
#dec=subcat['DELTA_J2000']
#starname=subcat['NUMBER']
# make region

def makeregion(filename) :
	
#	subcat=ascii.read(inimage[:-5]+'.cat')
	subcat=ascii.read(filename[:-5]+'.cat')

	#ra=subcat['ALPHA_J2000']
	#dec=subcat['DELTA_J2000']
	#starname=subcat['NUMBER']
	try : ra=list(subcat['col4'])
	except : ra=subcat['ALPHA_J2000']

	try : dec=list(subcat['col5'])
	except : dec=subcat['DELTA_J2000']
	
	try :starname=list(subcat['col1'])
	except : starname=subcat['NUMBER']
	

	radius=""" 7" """
	color="yellow"
	f=open(filename[:-5]+'.reg','w')
	head1="# Region file format: DS9 version 4.1\n"
	head2="""global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n"""
	head3="fk5\n"
	f.write(head1)
	f.write(head2)	
	f.write(head3)
	for n in range(len(ra)):
		body="circle("+str(ra[n])+","+str(dec[n])+","+radius+") # color="+color+" width=2 font=\"helvetica 10 normal roman\" text={"+str(starname[n])+"}\n"	
		f.write(body)
	f.close()

for images in inlist :
	makeregion(images)
 

# make jpg files

os.system('mkdir jpg')

def jpgreg(image) : 
	data=fits.getdata(image)

#	pl.imshow(data, cmap = mpl.cm.gray,origin='lower')
	obsdate = fits.getheader(image)['DATE-OBS']
	objname = fits.getheader(image)['OBJECT']
	subcat=ascii.read(image[:-5]+'.cat')

	#ra=subcat['ALPHA_J2000']
	#dec=subcat['DELTA_J2000']
	#starname=subcat['NUMBER']
	try : ra=list(subcat['col4'])
	except : ra=subcat['ALPHA_J2000']

	try : dec=list(subcat['col5'])
	except : dec=subcat['DELTA_J2000']
	
	try :starname=list(subcat['col1'])
	except : starname=subcat['NUMBER']
	fig = aplpy.FITSFigure(image)
	fig.set_theme('pretty')               #'publication'or 'pretty'
	fig.show_colorscale(cmap='gray',stretch='linear',pmin=1,pmax=99.5)
	fig.set_title(objname)
	radius = 0.002
	for r in range(len(ra)) :
		fig.show_circles(ra[r], dec[r], radius=0.003,color='yellow')
	
	#fig.show_regions(image[:-5]+'.reg')
	fig.add_label(0.5,0.95,image[17:],relative=True,color='orange',weight='bold')
	#fig.add_label(114.06621, -69.495733,'SN2015F',relative=False, color='yellow')
	#fig.show_circles(114.06621, -69.506733,15/3600.,layer='SN2015F',color='red')
	pl.savefig('jpg/'+image[:-5]+'.jpg')
	fig.close()

for images in inlist :
	jpgreg(images)
	print images

# reference
fig = aplpy.FITSFigure('ref2.fits')
objname = fits.getheader('ref2.fits')['OBJECT']
fig.set_theme('pretty')               #'publication'or 'pretty'
fig.show_colorscale(cmap='gray',stretch='linear',pmin=1,pmax=99.)
fig.set_title(objname)
fig.add_label(0.5,0.95,'ref.fits',relative=True,color='orange',weight='bold')
pl.savefig('jpg/ref.jpg')
fig.close()

os.system('mkdir jpg/com')
os.system('cp jpg/hd*.jpg jpg/com/')
os.system('cp jpg/ref.jpg jpg/com/')


print 'done'
print '\a'
