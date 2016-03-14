import os,sys
from astropy.io import ascii
import numpy as np
#sys.path.append("../.") # The directory that contains cosmic.py
#objlist=raw_input('give me the file list :')
#objlist='obj.list'
import cosmics
import pp
# Read the FITS :
	#filename="raCalibrated-T52-ceouobs.mim-ngc1097-20141030-012151-B-BIN1-W-300-001.fits"
os.system("ls tbgfz*.fits > obj.list")
os.system('rm ctbgfz*.fits')
	#infile=sys.argv[1]
	#os.system("ls rCalibrated*.fits > cosmicray.list")
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)
	#files=ascii.read(infile,guess=False)

# If you want the mask, here it is :
#cosmics.tofits(filename, c.mask, header)
# (c.mask is a boolean numpy array, that gets converted here to an integer array)

ppservers=()
ncpus=2
job_server = pp.Server(ncpus, ppservers=ppservers)
#job_server = pp.Server(ppservers=ppservers)

def lacosmic(filename) :
	print filename
	array, header = cosmics.fromfits(filename)
	# array is a 2D numpy array
	# Build the object :la cos
	c = cosmics.cosmicsimage(array, gain=1.45, readnoise=4.7, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0)
	# There are other options, check the manual...
	# Run the full artillery :
	c.run(maxiter = 4)
	# Write the cleaned image into a new FITS file, conserving the original header :
	cosmics.tofits('c'+filename, c.cleanarray, header)


jobs = [(input, job_server.submit(lacosmic, args=(input, ),modules=("cosmics", ))) for input in lists]


for input, job in jobs:
	job()


print '\a','Done!'
