# python code for file name change
# for Maidanak
# After fielding flat and Trimming images, Run this code.
# then, Remove CR and Solve Astrometry. 


from astropy.io import fits
import numpy as np
import sys
import os

'''
DATE-OBS= '2013-10-12'         /observed date (UT, beginning)
TIME-OBS= '19:50:60'           /observed time (UT, beginning)
OBJECT  = 'ngc0628 '           /object name
FILTER  =                    2 /1=U 2=B 3=V 4=R 5=I 6=N  0=unknown
EXPTIME =                60.00 /exposure time (sec)
'''

def fnamechange(fitsfile) :
	hdr=fits.getheader(fitsfile)
	dateobs=hdr['UTDATE']
	dateobs=dateobs[0:4]+dateobs[5:7]+dateobs[8:10]
	timeobs=hdr['UTSTART']
	timeobs=timeobs[0:2]+timeobs[3:5]+timeobs[6:8]
	objname=hdr['OBJECT']
	objname=objname.upper()	
	filname=str(hdr['FILTER'])
#	if filname == '2' : filname = 'B'
#	elif filname == '4' : filname = 'R'
	exptime=str(int(float(hdr['EXPTIME'])))
#	observa=hdr['OBSERVAT']
	observa='MAIDANAK'
	newname='Calibrated-'+observa+'-'+objname+'-'+dateobs+'-'+timeobs+'-'+filname+'-'+exptime+'.fits'
	sentence=fitsfile+' will be '+newname+'\n'    
	print sentence
	cpcom='cp '+fitsfile+' '+newname
	print cpcom	
	os.system(cpcom)

os.system('ls -d m* ngc* M* NGC* messier* IC* CGC* ic* ugc* UGC* PGC* MGC* IRAS* > direc.list')
alllist=np.genfromtxt('direc.list',usecols=(0),dtype=str)
for i in range(len(alllist)) :
	os.chdir(alllist[i])
	os.system("ls tbgfz*.fits > obj.list")
	infile='obj.list'
	files=np.genfromtxt(infile,usecols=(0),dtype=str)
	lists=list(files)

	for j in range(len(lists)) :
		fnamechange(lists[j])
	os.chdir('../')
os.system('python /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/8.go_lacosmic_maidanak_oneday.py')
	
