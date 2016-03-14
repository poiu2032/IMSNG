#xregister.py : iraf xregister task
#registration code
#

import numpy as np
import os,sys
from astropy.io import fits
from astropy.io import ascii
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import subprocess
from astropy.table import Table, Column
from astropy.time import Time
from pyraf import iraf
import numpy as np
import matplotlib.pyplot as plt

os.system('ls ahcCalibrate*.fits > obj.list')
objfile='obj.list'
resnum=subprocess.check_output('ls ahcCalibrate*.fits | wc -l',shell=True)
print "files astrometry done : ", resnum
objlist=np.genfromtxt(objfile,usecols=(0),dtype=str)
os.system('rm rah*.fits')

objlist=list(objlist)

def xregister(infile) :
	ref='ref.fits'
	region='[800:1000,350:490]'
#	inlist =(",".join(infile))
	outlist='r'+infile
	iraf.xregister.unlearn()
	iraf.xregister.setParam('input',infile)
	iraf.xregister.setParam('output',outlist)
	iraf.xregister.setParam('reference',ref)
	iraf.xregister.setParam('shifts','shift')
	iraf.xregister.setParam('regions',region)
	iraf.xregister.setParam('append','yes')
	iraf.wregister.setParam('mode','h')
	iraf.xregister(mode='h')

output=[]
for mm in range(len(objlist)) :
	#os.system('rm shift')
	xregister(objlist[mm])	
	#out='r'+objlist[mm]
	#output.append(out)
	#ref='ref.fits'
	#wrcom="wregister "+objlist[mm]+" "+output+" "+ref
	#infile=objlist[mm]	objlis	
	#print wrcom
	#xregister(infile)
	
print 'all done'
