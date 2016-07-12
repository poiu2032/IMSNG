import multiprocessing as mp
import os,sys
from astropy.io import ascii
import numpy as np
import cosmics
import pp

#sys.path.append("../.") # The directory that contains cosmic.py
#objlist=raw_input('give me the file list :')
#objlist='obj.list'
os.system("ls C*.fit > obj.list")
## infile=sys.argv[1]
## os.system("ls rCalibrated*.fits > cosmicray.list")
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

ppservers=()
ncpus=3
job_server = pp.Server(ncpus, ppservers=ppservers)

def lacosmic(filename) :
	import cosmics
	print filename
	array, header = cosmics.fromfits(filename)
	# array is a 2D numpy array
	# Build the object :la cos
	c = cosmics.cosmicsimage(array, gain=1.38, readnoise=10, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0)
	# There are other options, check the manual...
	# Run the full artillery :
	c.run(maxiter = 6)
	# Write the cleaned image into a new FITS file, conserving the original header :
	cosmics.tofits('c'+filename, c.cleanarray, header)
	print filename, 'done,'

'''
if __name__=='__main__':
	jobs = []
	for i in range(len(lists)) : 
		filename=lists[i]
		p=mp.Process(target=lacosmic,args=(filename,))
		jobs.append(p)
		p.start()
		#p.join()
'''

jobs = [(input, job_server.submit(lacosmic, args=(input, ),modules=("cosmics", ))) for input in lists]

for input, job in jobs:
        job()


print '\a'
