from astropy.io import ascii
import numpy as np
import os
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import multiprocessing as mp


os.system('ls recCal*.fits > obj.list')

os.system('rm hd*.fits')
os.system('rm hc*.fits')

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



if __name__=='__main__':
	jobs = []
	for i in range(len(infile)) : 
		filename=infile[i]
		p=mp.Process(target=hotpants,args=(filename,))
		jobs.append(p)
		p.start()





print 'all done, check it out!'
