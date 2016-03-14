# sextractor photometry and zp calculation from sdss converted Bmag (Lupton 2005)
# matching to reference cat of known star and find mag of PG0934+013
# edited by  Changsu from 2014/11/30 

from astropy.io import ascii
import os
import sys
from astropy.io import fits
import numpy as np
from astropy.time import Time
import robust
import matplotlib.pyplot as plt

#read all file list from obj.list
listfile='obj.list'
filelist=ascii.read(listfile,guess=False)
#lcogtfile=ascii.read('lcogtredobj.list')
fileid=filelist['obj.list']


f=open('photresult.txt','w')
f.write('filename jd psfmag pmagerr magat magaterr magap1 magap1err magap3 magap3err magap5 magap5err magap7 magap7err c1mag c1magerr c2mag c2magerr c3mag c3magerr sub \n')

#read info from file header
for n in range(len(fileid)) :
	files=fileid[n]
	header=fits.getheader(fileid[n])
	obsepoch=header['DATE-OBS']  #obs start time(utc)
	obsepoch=obsepoch.replace('T',' ')
	t=Time(obsepoch,format='iso',scale='utc')
	obsjd=t.jd
	print files,str(obsjd),'     ', str(n),' of ',str(len(fileid)),'\n,\n'

### shell command for sextracctor, psfex, stilts execution
	presecom="sex -c prepsfex.sex "+files+" -CATALOG_NAME "+files[:-5]+".cat"
	psfexcom="psfex -c default.psfex "+files[:-5]+".cat"
	postsecom="sex -psf_name "+files[:-5]+".psf -c phot.sex "+files+" -CATALOG_NAME "+files[:-5]+".cat"
	matchcom="stilts tskymatch2 ifmt1=ascii ifmt2=ascii in1=ref.cat in2="+files[:-5]+".cat out="+files[:-5]+".merge.cat ra1=RAJ2000 dec1=DEJ2000 ra2=col18 dec2=col19 error=1 join=1and2 ofmt=ascii omode=out"

#	print presecom
#	print psfexcom 
#	print postsecom
#	print matchcom

#	os.system(presecom)
#	os.system(psfexcom)
#	os.system(postsecom)
#	os.system(matchcom)
#os.system(matchorcom)

### zp and error calculation

	
	refcat='ref.cat'
	mergecat=files[:-5]+".merge.cat"
#mergecat=
	catread=ascii.read(mergecat)
	psfmag=catread['col32']
	psfmagerr=catread['col33']
	#automag=catread['col10']
	#automagerr=catread['col11']
	sdssmag=catread['sdssBmag']
	fwhmpix=catread['col21_2']
#psf
	pval=robust.mean(sdssmag - psfmag ,Cut=3.0)    #zp and error for one image
	pextmag=psfmag+pval[0]
	pextmagerr=np.sqrt(psfmagerr**2 + pval[1]**2)
#auto
	aval=robust.mean(sdssmag - automag ,Cut=3.0)    #zp and error for one image
	aextmag=automag+aval[0]
	aextmagerr=np.sqrt(automagerr**2 + aval[1]**2)


	inputcat=files[:-5]+'.cat'
	incatread=ascii.read(inputcat)
	smag=incatread['MAG_PSF']+val[0]
	smagerr=incatread['MAGERR_PSF']
	sra=incatread['ALPHA_J2000']
	sdec=incatread['DELTA_J2000']
	magat=incatread['MAG_AUTO']+val[0]
	magater=incatread['MAGERR_AUTO']
	magap1=incatread['MAG_APER']+val[0]
	magap3=incatread['MAG_APER_1']+val[0]
	magap5=incatread['MAG_APER_2']+val[0]
	magap7=incatread['MAG_APER_3']+val[0]
	magaper1=incatread['MAGERR_APER']
	magaper3=incatread['MAGERR_APER_1']
	magaper5=incatread['MAGERR_APER_2']
	magaper7=incatread['MAGERR_APER_3']
#target ra,dec
	tra=144.25437
	tdec=1.0954694
#distance from target 1" and minimum distance value from target : only one target!!
	dist=np.sqrt((sra-tra)**2+ (sdec-tdec)**2)
	idx=np.where((dist < (1/3600.)) & (dist==min(dist)))
	#idx=np.where((sra > 144.252) & (sra < 144.256) & (sdec > 1.094 ) & (sdec < 1.098))
	print smag[idx]
	fmag= float(smag[idx])
	ferr= float(np.sqrt(smagerr[idx]**2 + val[1]**2))
	magaterr=float(np.sqrt(magater[idx]**2 + val[1]**2))
	magap1err=float(np.sqrt(magaper1[idx]**2 + val[1]**2))
	magap3err=float(np.sqrt(magaper3[idx]**2 + val[1]**2))
	magap5err=float(np.sqrt(magaper5[idx]**2 + val[1]**2))
	magap7err=float(np.sqrt(magaper7[idx]**2 + val[1]**2))
	
	
	
	
	print 'Error= '+ str(np.sqrt(smagerr[idx]**2 + val[1]**2)) 

	photline=files+' '+str(obsjd)+' '+"%.4f" % fmag+' '+"%.4f" % ferr +' '+"%.4f" % magat[idx]+' '+"%.4f" % magaterr +' '+"%.4f" % magap1[idx]+' '+"%.4f" % magap1err +' '+"%.4f" % magap3[idx]+' '+"%.4f" % magap5err +' '+"%.4f" % magap5[idx]+' '+"%.4f" % magap5err +' '+"%.4f" % magap7[idx]+' '+"%.4f" % magap7err + '\n'
	f.write(photline)	


f.close()



#photdata=ascii.read('photresult.txt')
#jd=photdata['obsdate(ut,jd)']
#pmag=photdata['mag(psf)']
#perr=photdata['magerr']

#plt.errorbar(jd,pmag,yerr=perr)
#plt.show()

#sextractor for psfex
#psfex
#psf phot from image
#catalog matching

#zp point calculation

# all mag calibration

#object magnitude and other info, write to photresult.txt
