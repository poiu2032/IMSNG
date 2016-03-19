
#====================== Description =================================
# Author Changsu Choi, Modified by Gu Lim 2015
# The following two lines are only needed as cosmic.py is not in this directory nor in the python path.
# They would not be required if you copy cosmics.py in this directory.
# usage : python go_lacosmic.py obj.list
#==================== Source Codes ==================================
import os
import sys
from astropy.io import ascii
import numpy as np

sys.path.append("~/Desktop/IMSNG/9codes/automatic_1d_maidanak/") # The directory that contains cosmic.py
#objlist=raw_input('give me the file list :')
#objlist='obj.list'

import cosmics

# Read the FITS :
#filename="raCalibrated-T52-ceouobs.mim-ngc1097-20141030-012151-B-BIN1-W-300-001.fits"
#os.system("ls Calibrated*.fit > obj.list")

os.system('ls -d m* ngc* M* NGC* messier* IC* CGC* ic* ugc* UGC* PGC*  IRAS* > target.list')
target_list=np.genfromtxt('target.list',usecols=(0),dtype=str)

for i in range(len(target_list)) :
	os.chdir(target_list[i])

#infile=sys.argv[1]
	os.system("ls Calibrated*.fits > cosmicray.list")
#infile='obj.list'
	files=np.genfromtxt('cosmicray.list',usecols=(0),dtype=str)
	lists=list(files)
#files=ascii.read(infile,guess=False)
	j=0
	for j in range(len(lists)) :
		filename=lists[j]
		print filename
		array, header = cosmics.fromfits(filename)

	# array is a 2D numpy array

	# Build the object :
		c = cosmics.cosmicsimage(array, gain=1.38, readnoise=10, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0)
	# There are other options, check the manual...

	# Run the full artillery :
		c.run(maxiter = 4)

	# Write the cleaned image into a new FITS file, conserving the original header :
		cosmics.tofits('c'+filename, c.cleanarray, header)
	os.chdir('../')
print 'Job finished !'	
os.system('python /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/9.astrometry_1d_maidanak.py')
# If you want the mask, here it is :
#cosmics.tofits(filename, c.mask, header)
# (c.mask is a boolean numpy array, that gets converted here to an integer array)
