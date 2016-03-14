import os,sys
import numpy as np
from astropy.io import ascii
from astropy.io import fits
from astropy.time import Time
from astropy.io.votable import parse
from astropy.time import Time
import robust
import matplotlib.pyplot as plt


refcat='/data0/itelescope_data/t52/NGC2442/com/nomad.cat'
refim='ref.fits'


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

#	print "FWHM in pixel, ",fmp # , " FWHM in Arcsec, ",fmw, " pixel scale, ",ps
	return fmp


os.system('gethead rcC*.fits DATE-OBS filter exptime  > headinfo.txt')
os.system('ls rcCalibrated*.fits > inim.list')
os.system('ls hdrcCalibrated*.fits > subim.list')
tmpin  = np.genfromtxt('inim.list',usecols=(0),dtype=str)
inim   = list(tmpin)
inim.append('ref.fits')
tmpsub = np.genfromtxt('subim.list',usecols=(0),dtype=str)
subim   = list(tmpsub)

apersize='3,5,7,9,11,13,15,17,19,21'
detecthred = '5'
analthred  = '5'

#presecom="sex -c prepsfex.sex "+inimage+" -CATALOG_NAME "+inimage[:-5]+".cat"
#psfexcom="psfex -c default.psfex "+inimage[:-5]+".cat"
#sexcom='sex -c ../phot.sex '+inimage+' -CATALOG_NAME '+inimage[:-5]+'.cat -PARAMETERS_NAME  ../phot.param -psf_name '+inimage[:-5]+'.psf -seeing_fwhm '+str(fwhm)+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred+' -PHOT_APERTURES '+apersize 

#dualsexcom='sex -c ../phot.sex '+refim+' ,'+inimage+' -CATALOG_NAME dual'+inimage[:-5]+'.cat -PARAMETERS_NAME  ../phot.param -psf_name '+inimage[:-5]+'.psf -seeing_fwhm '+str(fwhm[i])+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred+' -PHOT_APERTURES '+apersize 

'''
error < 0.01
flag == 0
0.8 < stellarity < 1 
'''

fwhm = []
zp   = []
zperr= []
os.system("cp /data0/code/psfex.config/* .")
g=open('fwhm.txt','w')
for i in range(len(inim)) :
	inimage=inim[i]
	presecom="sex -c prepsfex.sex "+inimage+" -CATALOG_NAME "+inimage[:-5]+".cat"
	psfexcom="psfex -c default.psfex "+inimage[:-5]+".cat"
	os.system(presecom)
	os.system(psfexcom)
	os.system('cp psfex.xml '+inimage[:-5]+'.xml')	
	psfexxml(inimage[:-5]+'.xml')
	fwhm.append(psfexxml(inimage[:-5]+'.xml'))
	comment=inimage+'\t'+str(psfexxml(inimage[:-5]+'.xml'))
	g.write(comment+'\n')

	sexcom='sex -c ../phot.sex '+inimage+' -CATALOG_NAME '+inimage[:-5]+'.cat -PARAMETERS_NAME  ../phot.param -psf_name '+inimage[:-5]+'.psf -seeing_fwhm '+str(psfexxml(inimage[:-5]+'.xml'))+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred+' -PHOT_APERTURES '+apersize 
	#os.system(sexcom)
	dualsexcom='sex -c ../phot.sex '+refim+' , '+inimage+' -CATALOG_NAME dual'+inimage[:-5]+'.cat -PARAMETERS_NAME  ../phot.param -psf_name '+inimage[:-5]+'.psf -seeing_fwhm '+str(fwhm[i])+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred+' -PHOT_APERTURES '+apersize 
	#os.system(dualsexcom)
	
	matchcom="stilts tskymatch2 ifmt1=ascii ifmt2=ascii in1="+refcat+" in2="+inimage[:-5]+".cat out="+inimage[:-5]+".merge.cat ra1=RAJ2000 dec1=DEJ2000 ra2=col4 dec2=col5 error=1 join=1and2 ofmt=ascii omode=out"
	os.system(matchcom)	

	incat=ascii.read(inimage[:-5]+'.merge.cat')
	nomadmag   =incat['Bmag']	
	magauto    =incat['col8']
	magautoerr =incat['col9']
	flag       =incat['col16']
	stell      =incat['col20']
	index      =np.where((magautoerr < 0.02) & (flag==0) & (stell > 0.8 ))
	aval=robust.mean(nomadmag[index] - magauto[index] ,Cut=3.0)    #zp and error for one image
	
	aextmagerr=np.sqrt(magautoerr**2 + aval[1]**2)
	zp.append(aval[0])
	zperr.append(aval[1])	

g.close()

