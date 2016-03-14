# Edit image
from astropy.io import fits
import os
import sys
import numpy as np
from pyraf import iraf
import pp



ppservers=()
#ncpus
#ncpus=4
#make job_server
#job_server = pp.Server(ncpus, ppservers=ppservers)
job_server = pp.Server(ppservers=ppservers)


os.system('rm */t*.fits')
os.system('ls NGC*/*.fits  > obj.list')
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
objlist=list(objlist)

def imcopy(im) :
	from pyraf import iraf
	inim=im+'[6:4091, 60:4036]'
	im.split('/')
	outim=im.split('/')[0]+'/t'+im.split('/')[1]
	iraf.imcopy(inim,outim)


jobs = [(input, job_server.submit(imcopy, args=(input, ))) for input in objlist]


# for loop of function in job using multi-core
for input, job in jobs:
	job()

