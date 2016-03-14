# The following two lines are only needed as cosmic.py is not in this directory nor in the python path.
# They would not be required if you copy cosmics.py in this directory.
# usage : python go_lacosmic.py obj.list
#
import os,sys
from astropy.io import ascii
import numpy as np
#sys.path.append("../.") # The directory that contains cosmic.py
#objlist=raw_input('give me the file list :')
#objlist='obj.list'
import cosmics

# Read the FITS :
#filename="raCalibrated-T52-ceouobs.mim-ngc1097-20141030-012151-B-BIN1-W-300-001.fits"
os.system("ls Calibrated*.fits > obj.list")
#infile=sys.argv[1]
#os.system("ls rCalibrated*.fits > cosmicray.list")
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)
#files=ascii.read(infile,guess=False)
i=0
for i in range(len(lists)) :
	filename=lists[i]
	print filename
	array, header = cosmics.fromfits(filename)

	# array is a 2D numpy array

	# Build the object :
	c = cosmics.cosmicsimage(array, gain=1.0, readnoise=3.5, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0)
	# There are other options, check the manual...

	# Run the full artillery :
	c.run(maxiter = 4)

	# Write the cleaned image into a new FITS file, conserving the original header :
	cosmics.tofits('c'+filename, c.cleanarray, header)

# If you want the mask, here it is :
#cosmics.tofits(filename, c.mask, header)
# (c.mask is a boolean numpy array, that gets converted here to an integer array)
