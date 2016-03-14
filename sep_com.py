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


def imcombine(group,output):
	group=(",".join(group))
#	combine=average
	iraf.imcombine.setParam('input',group)
	iraf.imcombine.setParam('output',output)
	iraf.imcombine.setParam('combine','median')
#	iraf.imcombine.setParam('combine',combine)
#	iraf.imcombine.setParam('combine','average')
	iraf.imcombine.setParam('reject','minmax')
	iraf.imcombine(group,output=output)


os.system('gethead cCalibrated*.fits filter exptime date-obs > info.txt')
info=ascii.read('info.txt')
info.sort('col4')
filename = info['col1']
filters  = info['col2']
exptime  = info['col3']
obstime  = info['col4']

t = Time(obstime, format='isot', scale='utc')
datestr,timestr=[],[]

for tt in t :
	datestr.append(str(tt)[0:10])
	timestr.append(str(tt)[11:24]) 




tjd=t.mjd
tcen=tjd+((exptime/2)/86400.)

tmpgroup=[]
groupdic={}
k=0
for i in range(len(tjd)) :
	if (tjd[i] - tjd[k]) < (15./1440.) 	:
		tmpgroup.append(filename[i])
	else : k=k+1
	
		
		



