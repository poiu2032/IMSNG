# Flat File Organization

import os
import sys
import numpy as np
print '='*73
print '|          [P]reprocessing [P]ipeline for [M]aidanak [O]bservatory      |'
print '|                 Changsu Choi, G. Lim 2013 - 2016                      |'
print '|                   Dept. of Physics & Astronomy                        |'
print '|                  Seoul National University (SNU)                      |'
print '|    Center for the Exploration of the Origin of the Universe (CEOU)    |'
print '='*73



print 'Flat file organization starts...'
os.system('mkdir fakeflat1 fakeflat2 flat1 flat2') # to avoid error while running np.genfromtxt
os.system('ls -d fakeflat1 fakeflat2 flat flat1 flat2 > flat.dir')

flatlist=np.genfromtxt('flat.dir',usecols=(0),dtype=str)


if 'flat1' and 'flat2' in flatlist :
	os.system('mv ./flat2/*.fits ./flat1/')
	os.system('mv flat1 flat')
	print 'Files in flat 2 is moved to flat1 !'
'''
elif 'flat1' in flatlist and 'flat2' not in flatlist :
	os.system('mv flat1 flat')
	print 'Only flat1 changed its name flat !'
elif 'flat1' not in flatlist and 'flat2' in flatlist :
	os.system('mv flat2 flat')
	print 'Only flat2 changed its name flat !'
'''
if 'flat1' and 'flat2' not in flatlist :
	print 'There is nothing ! Move flats from adjacent directories !!'

	
print 'File Organization is complete ! Run maidanak_process.cl !'
os.system('rmdir fakeflat1 fakeflat2')
os.system('rm flat.dir')

