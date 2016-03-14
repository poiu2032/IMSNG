from astropy.io import fits
from pyraf import iraf
import os
import numpy as np
os.system('rm *_aa.fits')
os.system('rm *_bb.fits')
os.system('rm *_cc.fits')
os.system('rm *_dd.fits')

#filename='test.fits'
filelist=np.genfromtxt('filelist.txt',usecols=(0),dtype=str)


aa = '[1:2047,41:2047]'
bb = '[2048:4096,41:2047]'
cc = '[1:2047,2048:4056]'
dd = '[2048:4096,2048:4056]'

regions = ['[1:2047,41:2047]', '[2048:4096,41:2047]', '[1:2047,2048:4056]', '[2048:4096,2048:4056]']

quadname= ['aa','bb','cc','dd']
#quadname='aa'

def imcopy(filename,region,quadname) :
	inputname=filename+region
	iraf.imutil.imcopy.setParam('input',inputname)
	iraf.imutil.imcopy.setParam('output',filename[:-5]+'_'+quadname+'.fits')
	iraf.imutil.imcopy(mode='h')


for files in filelist :
	
	for q in range(len(quadname)) :
		imcopy(files,regions[q],quadname[q])




