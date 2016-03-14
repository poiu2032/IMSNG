import numpy as np
from astropy.io import fits
from astropy.io import ascii
import os
import sys
from pyraf import iraf


'''
SIMPLE  =                    T / Fits standard
BITPIX  =                  -32 / Bits per pixel
NAXIS   =                    2 / Number of axes
NAXIS1  =                 4096 / Axis length
NAXIS2  =                 4096 / Axis length
EXTEND  =                    F / File may contain extensions
ORIGIN  = 'NOAO-IRAF FITS Image Kernel July 2003' / FITS file originator
DATE    = '2015-08-30T13:31:53' / Date FITS file was generated
IRAF-TLM= '2015-08-30T13:31:52' / Time of last modification
GAIN    = '1.43    '
RDNOISE = '13.6    '
INSTRUME= 'FLI     ' /          instrument or camera used
DATE-OBS= '2014-11-02T19:57:28' /YYYY-MM-DDThh:mm:ss observation start, UT
EXPTIME =   60.000000000000000 /Exposure time in seconds
EXPOSURE=   60.000000000000000 /Exposure time in seconds
SET-TEMP=  -30.000000000000000 /CCD temperature setpoint in C
CCD-TEMP=  -30.000000000000000 /CCD temperature at start of exposure in C
XPIXSZ  =   9.0000000000000000 /Pixel Width in microns (after binning)
YPIXSZ  =   9.0000000000000000 /Pixel Height in microns (after binning)
XBINNING=                    1 /Binning factor in width
YBINNING=                    1 /Binning factor in height
XORGSUBF=                    0 /Subframe X position in binned pixels
YORGSUBF=                    0 /Subframe Y position in binned pixels
IMAGETYP= 'Light Frame' /       Type of image
'''

os.system('ls fd*.fits > obj.list')
alllist=np.genfromtxt('obj.list',usecols=(0),dtype=str)

#fdngc3183-002R.fits
#acCalibrated-SOAO-NGC0337-20131012-175023-R-60.fits

def fnamechange(fitsfile) :
	hdr=fits.getheader(fitsfile)
	dateobs=hdr['DATE-OBS']
	dateobs=dateobs[0:4]+dateobs[5:7]+dateobs[8:10]+'-'+dateobs[11:13]+dateobs[14:16]+dateobs[17:19]
	objname=str(files[2:-10])
	objname=objname.upper()	
	filname=files[-6]
	exptime=str(int(hdr['EXPTIME']))
	observa='SOAO'
	newname='Calibrated-'+observa+'-'+objname+'-'+dateobs+'-'+filname+'-'+exptime+'.fits'
	sentence=fitsfile+' will be '+newname+'\n'    
	print sentence
	cpcom='cp '+fitsfile+' '+newname
	print cpcom	
	os.system(cpcom)
'''
os.system("ls fd*.fits > obj.list")
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)
'''
for files in alllist :
	fnamechange(files)

print 'all done'
print '\a'
