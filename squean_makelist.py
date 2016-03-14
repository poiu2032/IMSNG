# squean filelist making code
# usage : squean_makelist.py filelist file_num1.fits file_num2.fits
# ex) squean_makelist.py bias.list 20151013_0105.fits 20151013_0110.fits  
# makes a filelist of files starting from lower number to higher number, 
# for example from 105-110
# file list of [105.fits, 106.fits, 107.fits, 108.fits, 109.fits, 110.fits ]
# will be created


import astropy.io.fits as fits
import numpy as np
from pyraf import iraf
from iraf import imred, ccdred
import os 
import sys

outlist= sys.argv[1]
filenum1 = sys.argv[2]
filenum2 = sys.argv[3]

num1=int(filenum1[9:-5])
num2=int(filenum2[9:-5])


k=open(outlist,'w')

while num1 <= num2 :
	print '%0.4i'%int(num1)
	k.write(filenum1[0:9]+'%0.4i'%int(num1)+filenum1[13:18]+'\n')
	num1=num1+1

k.close()
print '\a', 'Check the file.'
print outlist
os.system('cat '+outlist)

