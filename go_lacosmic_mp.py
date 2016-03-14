import multiprocessing as mp
import os,sys
from astropy.io import ascii
import numpy as np
import cosmics


#sys.path.append("../.") # The directory that contains cosmic.py
#objlist=raw_input('give me the file list :')
#objlist='obj.list'
os.system("ls Calibrated*.fit > obj.list")
os.system('rm cCal*.fit')
## infile=sys.argv[1]
## os.system("ls rCalibrated*.fits > cosmicray.list")
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

def lacosmic(filename) :
	import cosmics
	print filename
	array, header = cosmics.fromfits(filename)
	# array is a 2D numpy array
	# Build the object :la cos
	c = cosmics.cosmicsimage(array, gain=1.38, readnoise=10, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0)
	# There are other options, check the manual...
	# Run the full artillery :
	c.run(maxiter = 4)
	# Write the cleaned image into a new FITS file, conserving the original header :
	cosmics.tofits('c'+filename, c.cleanarray, header)
	print filename, 'done,'


if __name__=='__main__':
	jobs = []
	for i in range(len(lists)) : 
		filename=lists[i]
		p=mp.Process(target=lacosmic,args=(filename,))
		jobs.append(p)
		p.start()
		#p.join()
print '\a'
