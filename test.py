#call for cCalibated~*.fits after cosmicray removal and astrometry
#code for registration and convolution then subtraction
#need reference frame 'ref.fits' from 'makeref.py'
#wregister 
#psfex for fwhm value : fwhm.txt
#convolution and sutraction hc, hd~ with HOTPANTS

from astropy.io import ascii
import os
import sys
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
from astropy.time import Time
from astropy.io import ascii
from astropy.table import Table, Column
from astropy.io.votable import parse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import interpolate
from pyraf import iraf



def psfexxml(xmlfile):
	votable=parse(xmlfile)
	table=votable.get_first_table()
	data= table.array
	table=votable.get_first_table()
	data= table.array

	data['FWHM_Mean']
	fmp=data['FWHM_Mean'][0]
	#fmw=data['FWHM_WCS_Mean'][0] 
	#ps=data['PixelScale_WCS_Mean'][0]
	#em=data['Ellipticity_Mean'][0]

	print "FWHM in pixel, ",fmp # , " FWHM in Arcsec, ",fmw, " pixel scale, ",ps
	return fmp

def gauss(group,output,sigma):
#	group=(",".join(group))
#	output=
#	combine=average
	iraf.gauss.setParam('input',group)
	iraf.gauss.setParam('output',output)
	iraf.gauss.setParam('sigma',sigma)
	iraf.gauss.setParam('nsigma',4)
#	iraf.gauss.setParam('combine',combine)
#	iraf.gauss.setParam('combine','average')
#	iraf.gauss.setParam('reject','minmax')
	iraf.gauss(group,output,sigma)

def sub(im,sub,out):
	iraf.imutil()
	iraf.imutil.imarith.setParam('operand1',im)
	iraf.imutil.imarith.setParam('op','-')
	iraf.imutil.imarith.setParam('operand2',sub)
	iraf.imutil.imarith.setParam('result',out)
	iraf.imutil.imarith(mode='h')

def multiple(im,num,out):
	iraf.imutil()
	iraf.imutil.imarith.setParam('operand1',im)
	iraf.imutil.imarith.setParam('op','*')
	iraf.imutil.imarith.setParam('operand2',num)
	iraf.imutil.imarith.setParam('result',out)
	iraf.imutil.imarith(mode='h')

	
def wregister(infile,ref,output) :
	#inlist=(",".join(inlist))
	#output=(",".join(output))
	iraf.wregister.unlearn()
	iraf.wregister.setParam('input',infile)
	iraf.wregister.setParam('output',output)
	iraf.wregister.setParam('reference',ref)
	#iraf.wregister.setParam('mode','')
	iraf.wregister(infile,ref,output)


#print gg
#inlist=[]

	
os.system("ls cCalibrate*.fits > obj.list")	
infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

inlist=list(files)
for mm in range(len(inlist)) :
	output='r'+inlist[mm]
	ref="ref.fits"
	wrcom="wregister "+inlist[mm]+" "+output+" "+ref
	infile=inlist[mm]		
	print wrcom
	wregister(infile,ref,output)


fwhm=[]
os.system("cp /data0/psfex.config/* .")
g=open('fwhm.txt','w')
for i in range(len(lists)) :
	files=lists[i]
	presecom="sex -c prepsfex.sex "+files+" -CATALOG_NAME "+files[:-5]+".cat"
	psfexcom="psfex -c default.psfex "+files[:-5]+".cat"
	os.system(presecom)
	os.system(psfexcom)
	os.system('cp psfex.xml '+files[:-5]+'.xml')
	psfexxml(files[:-5]+'.xml')
	fwhm.append(psfexxml(files[:-5]+'.xml'))
	comment=lists[i]+'\t'+str(psfexxml(files[:-5]+'.xml'))
	g.write(comment+'\n')
g.close()

'''
pixscale=0.4814
fluxratio=[]
for i in range(len(lists)) :
	fw=fwhm[i]*pixscale
	secom="sex -c default.sex "+lists[i]+" -DETECT_THRESH 5 -ANALYSIS_THRESH 5 -PIXEL_SCALE 0 -SEEING_FWHM "+str(fw)+" -CATALOG_NAME pre"+lists[i][:-5]+".cat"
	os.system(secom)
	data=ascii.read("pre"+lists[i][:-5]+".cat")
	num=len(data['NUMBER'])
	mag=data['MAG_AUTO']

	print num, min(mag)
	
	matchcom="stilts tskymatch2 ifmt1=ascii ifmt2=ascii in1=sub.cat in2=pre"+lists[i][:-5]+".cat out="+lists[i][:-5]+".merge.cat ra1=col8 dec1=col9 ra2=col8 dec2=col9 error=1 join=1and2 ofmt=ascii omode=out"
	#os.system("starlink")
	#os.system(matchcom)
	
	mergecat=lists[i][:-5]+".merge.cat"
	mdata=ascii.read(mergecat)
	reffluxaver=mdata['col2_1']
	varfluxaver=mdata['col2_2']
	fluxratio.append(np.average(reffluxaver) / np.average(varfluxaver))
	


	
# reference frame, the least fwhm value
idx=np.where(fwhm==min(fwhm))

#idx1=idx[0][0]
idx1=0
os.system('cp '+lists[idx1]+' ref.fits')
print 'reference frame will be : ',lists[idx1],fwhm[idx1]

os.system('rm -rf conv*.fits')
os.system('rm -rf subconv*.fits')
sigmavar=[]
fwhm[i]=fwhm[i]/2.35482
for i in range(len(lists)) :
	smoothing=np.sqrt(fwhm[i]**2 - fwhm[idx1]**2  )
	sigma=smoothing 
	output='conv'+lists[i]
	if idx1 == i : sigma = 1
	gauss(lists[i],output,sigma)
	#multiout='b'+output
	#subout='su'+multiout
	subout='sub'+output
	#multiple(lists[i],fluxratio[i],multiout)
	#sub(lists[i],multiout,subout)
	sub(lists[i],output,subout)
	sigmavar.append(sigma)	
	print lists[i],sigma

for i in range(len(lists)) :
	print lists[i],sigmavar[i] 

os.system('ds9 subconv*.fits &')



from astropy.convolution import convolve, convolve_fft


#result = convolve(image, kernel)

'''
os.system('ls rcC*.fits > obj.list')

objfile='obj.list'
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
infile=objlist

for n in range(len(infile)):
	outfile='hd'+infile[n]
	convfile='hc'+infile[n]
	com='hotpants -inim '+infile[n]+' -tmplim ref.fits -outim '+outfile+' -oci '+convfile
	print infile[n]
	os.system(com)
	
os.system('ds9 hdrcC*.fits &')	

