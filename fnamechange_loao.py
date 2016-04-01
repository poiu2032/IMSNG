# python code for file name change
# for LOAO 
from astropy.io import fits
import numpy as np
import sys
import os

'''
DATE-OBS= '2015-09-30T08:24:22.079375' / UT Date/time of Observation
FILTER  = 'R104    '           / R=R104 B=B102
EXP_TIME=                  60. / Length of Exposure
'''

def fnamechange(fitsfile) :
	hdr=fits.getheader(fitsfile)
	dateobs=hdr['DATE-OBS']

        dateobs=dateobs[11:13]+dateobs[14:16]+dateobs[17:19]

#	dateobs=dateobs[0:4]+dateobs[5:7]+dateobs[8:10]
#	timeobs=hdr['TIME-OBS']
#	timeobs=dateobs[11:13]+dateobs[14:16]+dateobs[17:19]
#	objname=hdr['OBJECT']
#	objname=objname.upper()	
	filname=str(hdr['FILTER'])
	if filname == 'B102' : filname = 'B'
	elif filname == 'R104' : filname = 'R'

	if 'EXP_TIME' in hdr : exptime=str(int(hdr['EXP_TIME']))
	else : exptime='Na'
	
	newname=fitsfile[0:len(fitsfile)-5]+'-'+dateobs+'-'+filname[0:1]+'-'+exptime+'.fits'
#	newname=fitsfile[0:len(fitsfile)-30]+'-'+dateobs+'-'+filname[0:1]+'-'+exptime+'.fits'
#	newname=fitsfile[0:len(fitsfile)-17]+'.fits'

	sentence=fitsfile+' will be '+newname+'\n'    
	print sentence
	mvcom='mv '+fitsfile+' '+newname
	print mvcom	
	os.system(mvcom)


os.system("ls *bj*.fits > obj.list")
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

for i in range(len(lists)) :
	fnamechange(lists[i])
