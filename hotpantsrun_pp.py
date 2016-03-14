from astropy.io import ascii
import numpy as np
import os
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import pp

ppservers=()
# cpu counting
ncpus=2
#make job_server
job_server = pp.Server(ncpus, ppservers=ppservers)
#job_server = pp.Server(ppservers=ppservers)


os.system('ls reahacCal*.fits > obj.list')

os.system('rm hdreahacCal*.fits')
os.system('rm hcreahacCal*.fits')

objfile='obj.list'
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
infile=objlist

	
def hotpants(infile) :
	outfile='hd'+infile
	convfile='hc'+infile
	com='hotpants -v 0 -inim '+infile+' -tmplim ref.fits -outim '+outfile+' -oci '+convfile
	#com='hotpants -v 0 -c i -n i -inim '+infile[n]+' -tmplim ref.fits -outim '+outfile+' -oci '+convfile
	print 'doing HOTPANTS work for ',infile
	os.system(com)




jobs = [(input, job_server.submit(hotpants, args=(input, ),modules=("os", ))) for input in infile]

# for loop of function in job using multi-core
for input, job in jobs:
	job()

print 'all done, check it out!'
