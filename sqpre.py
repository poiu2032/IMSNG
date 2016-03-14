#Gain : 1.0
#RDnoise : 8.2

import os
import sys
import glob
import numpy as np
from astropy.io import ascii
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table, Column
from astropy.time import Time
from pyraf import iraf

alllist=glob.glob('201*.fits')
os.system('gethead OBSTYPE OBJECT EXPTIME DATE-OBS TIME-OBS FILTER TEL_RA TEL_DEC AIRMASS 201*.fits > allinfo.txt')
allinfo=ascii.read('allinfo.txt')
info=Table(allinfo)

datetime=[]
for n in range(len(info['col5'])) :
	datetime.append( info['col5'][n]+'T'+info['col6'][n]) 

indbias=np.where(info['col2'] == 'BIAS')
biaslist=info['col1'][indbias]

datetime[indbias]

	
