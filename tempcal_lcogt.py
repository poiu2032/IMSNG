from astropy.io import ascii
import os
import sys
from astropy.io import fits
import numpy as np
from astropy.time import Time
import robust
from astropy.io.votable import parse
#import matplotlib.pyplot as plt

#read all file list from obj.list
listfile='obj.list'
objlist=np.genfromtxt('obj.list',usecols=(0),dtype=str)
#filelist=ascii.read(listfile,guess=False,)
#lcogtfile=ascii.read('lcogtredobj.list')
fileid=objlist

pathstr=os.getcwd()
if pathstr=='/data1/Documents/PG0934+013/PHOTOMETRY/process/LOAO/redimage' :
	outfile='../../../photresult_loao.txt'
else :
	outfile='../../../photresult_lcogt.txt'

print outfile,'\n'

f=open(outfile,'w')
f.write('#filename jd magat magaterr  magap5 magap5err magap7 magap7err cmag cdelmag cdelmagrms cmagerrmean delmagmean delmagrms apnum wmean werr \n')

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
	presecom="sex -c prepsfex.sex "+files+"[0] -CATALOG_NAME "+files[:-5]+".cat"
	psfexcom="psfex -c default.psfex "+files[:-5]+".cat"
	postsecom="sex -psf_name "+files[:-5]+".psf -c phot.sex "+files+" -CATALOG_NAME "+files[:-5]+".cat"
	matchcom="stilts tskymatch2 ifmt1=ascii ifmt2=ascii in1=ref.cat in2="+files[:-5]+".cat out="+files[:-5]+".merge.cat ra1=RAJ2000 dec1=DEJ2000 ra2=col18 dec2=col19 error=1 join=1and2 ofmt=ascii omode=out"

#	print presecom
#	print psfexcom 
#	print postsecom
#	print matchcom

#	os.system(presecom)
#	os.system(psfexcom)
#	print postsecom
#	os.system(postsecom)
#	print matchcom
#	os.system(matchcom)
#os.system(matchorcom)

### zp and error calculation

	
	refcat='ref.cat'
	mergecat=files[:-5]+".merge.cat"
	catread=ascii.read(mergecat)
#mergecat=
	sra=catread['col18_2']
	sdec=catread['col19_2']
	catread=ascii.read(mergecat)
	psfmag=catread['col32']
	psfmagerr=catread['col33']
	automag=catread['col10_2']
	automagerr=catread['col11_2']
	sdssmag=catread['sdssBmag']
	ap1mag=catread['col4_2']
	ap2mag=catread['col5_2']
	ap1magerr=catread['col8_2']
	ap2magerr=catread['col9_2']	
	if pathstr=='/data1/Documents/PG0934+013/PHOTOMETRY/process/LOAO/redimage' :
		apmag=ap1mag
		apmagerr=ap1magerr
	else :
		apmag=ap2mag
		apmagerr=ap2magerr
#	fwhmpix=catread['col21_2']
#	ind=np.where(automagerr < 0.01)
# 	fwhm0=fwhmpix.data.data(ind)
#	#print len(fwhmpix),len(fwhm0)
#	fwhm1=robust.mean(fwhm0,Cut=3.0)
#	print len(fwhmpix),len(fwhm0), fwhm1[0], fwhm1[1]
	
#psf
	pval=robust.mean(sdssmag - psfmag ,Cut=3.0)    #zp and error for one image
	pextmag=psfmag+pval[0]
	pextmagerr=np.sqrt(psfmagerr**2 + pval[1]**2)
#auto
	aval=robust.mean(sdssmag - automag ,Cut=3.0)    #zp and error for one image
	aextmag=automag+aval[0]
	aextmagerr=np.sqrt(automagerr**2 + aval[1]**2)
	val=aval

#apmag	
	apval=robust.mean(sdssmag - apmag ,Cut=3.0)    #zp and error for one image
	apintmag=apmag+apval[0]
	apintmagerr=np.sqrt(apmagerr**2 + apval[1]**2)

	apintval=apval
	apnum=len(apmag)
	delmag= apintmag - sdssmag
	delmagmean=np.mean(delmag)
	delmagrms=np.sqrt(sum(delmag**2))/apnum

#weighted mean calculation
	wmean=sum((sdssmag-apmag)/apmagerr**2)/(sum(1./apmagerr**2))
	werr=np.sqrt(1./(sum(1./apmagerr**2)))
	print 'weighted values and number of stars used : ',wmean, werr,apnum
	wval=apmag+wmean
	wmagerr=np.sqrt(apmagerr**2 + werr**2)

#target ra,dec
	tra=144.25437
	tdec=1.0954694
	cra=144.2953
	cdec=1.051096
	c1ra, c1dec=144.2953, 1.051096
	c2ra, c2dec=144.18559, 1.106457
	c3ra, c3dec=144.22666, 1.146373
	c4ra, c4dec=144.194324, 1.055098  #, 10" ) # color=yellow text={1}
	c5ra, c5dec=144.225342, 1.042914  #, 10" ) # color=yellow text={2}
	c6ra, c6dec=144.235911, 1.080229  #, 10" ) # color=yellow text={4}
	c7ra, c7dec=144.250951, 1.015701  #, 10" ) # color=yellow text={5}
	c8ra, c8dec=144.307824, 1.14705   #, 10" ) # color=yellow text={7}
	c9ra, c9dec=144.311101, 1.021975  #, 10" ) # color=yellow text={8}
	c0ra, c0dec=144.320857, 1.027026  #, 10" ) # color=yellow text={9}

	c1dist=np.sqrt((sra-c1ra)**2+ (sdec-c1dec)**2)
	c1idx=np.where((c1dist < (1/3600.)) & (c1dist==min(c1dist)))
	c2dist=np.sqrt((sra-c2ra)**2+ (sdec-c2dec)**2)
	c2idx=np.where((c2dist < (1/3600.)) & (c2dist==min(c2dist)))
	c3dist=np.sqrt((sra-c3ra)**2+ (sdec-c3dec)**2)
	c3idx=np.where((c3dist < (1/3600.)) & (c3dist==min(c3dist)))
#	c4dist=np.sqrt((sra-c4ra)**2+ (sdec-c4dec)**2)
#	c4idx=np.where((c4dist < (1/3600.)) & (c4dist==min(c4dist)))
	c5dist=np.sqrt((sra-c5ra)**2+ (sdec-c5dec)**2)
	c5idx=np.where((c5dist < (1/3600.)) & (c5dist==min(c5dist)))
	c6dist=np.sqrt((sra-c6ra)**2+ (sdec-c6dec)**2)
	c6idx=np.where((c6dist < (1/3600.)) & (c6dist==min(c6dist)))
#	c7dist=np.sqrt((sra-c7ra)**2+ (sdec-c7dec)**2)
#	c7idx=np.where((c7dist < (1/3600.)) & (c7dist==min(c7dist)))
	c8dist=np.sqrt((sra-c8ra)**2+ (sdec-c8dec)**2)
	c8idx=np.where((c8dist < (1/3600.)) & (c8dist==min(c8dist)))
	c9dist=np.sqrt((sra-c9ra)**2+ (sdec-c9dec)**2)
	c9idx=np.where((c9dist < (1/3600.)) & (c9dist==min(c9dist)))
	c0dist=np.sqrt((sra-c0ra)**2+ (sdec-c0dec)**2)
	c0idx=np.where((c0dist < (1/3600.)) & (c0dist==min(c0dist)))

	c0mag, c0magerr= float(apmag[c0idx])+ wmean, np.sqrt((float(apmagerr[c0idx])**2 )+werr**2)
	c1mag, c1magerr= float(apmag[c1idx])+ wmean, np.sqrt((float(apmagerr[c1idx])**2 )+werr**2)
	c2mag, c2magerr= float(apmag[c2idx])+ wmean, np.sqrt((float(apmagerr[c2idx])**2 )+werr**2)
	c3mag, c3magerr= float(apmag[c3idx])+ wmean, np.sqrt((float(apmagerr[c3idx])**2 )+werr**2)
#	c4mag, c4magerr= float(apmag[c1idx])+ wmean, np.sqrt((float(apmagerr[c1idx])**2 )+werr**2)
	c5mag, c5magerr= float(apmag[c1idx])+ wmean, np.sqrt((float(apmagerr[c1idx])**2 )+werr**2)	
	c6mag, c6magerr= float(apmag[c1idx])+ wmean, np.sqrt((float(apmagerr[c1idx])**2 )+werr**2)
#	c7mag, c7magerr= float(apmag[c1idx])+ wmean, np.sqrt((float(apmagerr[c1idx])**2 )+werr**2)
	c8mag, c8magerr= float(apmag[c2idx])+ wmean, np.sqrt((float(apmagerr[c2idx])**2 )+werr**2)
	c9mag, c9magerr= float(apmag[c3idx])+ wmean, np.sqrt((float(apmagerr[c3idx])**2 )+werr**2)
	cmagarr=[c1mag,c2mag,c3mag,c5mag,c6mag,c8mag,c9mag,c0mag]
	cmag=(c1mag+c2mag+c3mag+c5mag+c6mag+c8mag+c9mag+c0mag)/len(cmagarr)
	cdelmag=((c1mag-sdssmag[c1idx][0])+(c2mag-sdssmag[c2idx][0])+(c3mag-sdssmag[c3idx][0])+(c5mag-sdssmag[c5idx][0])+(c6mag-sdssmag[c6idx][0])+(c8mag-sdssmag[c8idx][0])+(c9mag-sdssmag[c9idx][0])+(c0mag-sdssmag[c0idx][0]) )/len(cmagarr)
	cdelmagrms=np.sqrt(  (c1mag-sdssmag[c1idx][0])**2+(c2mag-sdssmag[c2idx][0])**2+(c3mag-sdssmag[c3idx][0])**2+(c5mag-sdssmag[c5idx][0])**2+(c6mag-sdssmag[c6idx][0])**2+(c8mag-sdssmag[c8idx][0])**2+(c9mag-sdssmag[c9idx][0])**2+(c0mag-sdssmag[c0idx][0])**2 )/len(cmagarr)
	cmagerrmean=(c1magerr+c2magerr+c3magerr+c5magerr+c6magerr++c8magerr+c9magerr+c0magerr)/len(cmagarr)	
	print 'cmag ', cmag, 'del mag ', cdelmag, 'del mag rms ',cdelmagrms,'mag error mean ', cmagerrmean
'''
	dm_wmean
	dm_wmeanrms
	c1mag
	c2mag
	c3mag
	c1err
	c2err
	c3err
'''	
	

#input catalog
	inputcat=files[:-5]+'.cat'
	incatread=ascii.read(inputcat)
	smag=incatread['MAG_PSF']+val[0]
	smagerr=incatread['MAGERR_PSF']

	smag1=incatread['MAG_AUTO']+val[0]
	smagerr1=incatread['MAGERR_AUTO']
	wcmag=incatread['MAG_AUTO']+wmean
	
	sra=incatread['ALPHA_J2000']
	sdec=incatread['DELTA_J2000']
#	magat=incatread['MAG_AUTO']+val[0]
	magat=incatread['MAG_AUTO']+wmean
	magater=incatread['MAGERR_AUTO']
	magater=np.sqrt(magater**2 + werr**2)
	magap1=incatread['MAG_APER']+val[0]
	magap3=incatread['MAG_APER_1']+val[0]
	magap5=incatread['MAG_APER_2']+wmean
	magap7=incatread['MAG_APER_3']+wmean
	magaper1=incatread['MAGERR_APER']
	magaper3=incatread['MAGERR_APER_1']
	magaper5=incatread['MAGERR_APER_2']
	magaper7=incatread['MAGERR_APER_3']
	fwhmpix=incatread['FWHM_IMAGE']
	ind=np.where(magater < 0.01)
 	fwhm0=fwhmpix[ind]
	#print len(fwhmpix),len(fwhm0)
	#fwhm1=robust.mean(fwhm0,Cut=3.0)


	
	cmagerr= np.sqrt(c1magerr**2+ c2magerr**2 + c3magerr**2)/np.sqrt(3.)
	#idx=np.where((sra > 144.252) & (sra < 144.256) & (sdec > 1.094 ) & (sdec < 1.098))
	
	#cmag=float(smag[cidx])	
	#cmagerr=float(np.sqrt(smagerr[cidx]**2 + val[1]**2))
#distance from target 1" and minimum distance value from target : only one target!!
	dist=np.sqrt((sra-tra)**2+ (sdec-tdec)**2)
	idx=np.where((dist < (1/3600.)) & (dist==min(dist)))

	#fmag= float(smag[idx])
	#ferr= float(np.sqrt(smagerr[idx]**2 + val[1]**2))
	magaterr =float(np.sqrt(magater[idx]**2  + werr**2))
	magap1err=float(np.sqrt(magaper1[idx]**2 + werr**2))
	magap3err=float(np.sqrt(magaper3[idx]**2 + werr**2))
	magap5err=float(np.sqrt(magaper5[idx]**2 + werr**2))
	magap7err=float(np.sqrt(magaper7[idx]**2 + werr**2))
	sub=float(magat[idx])-float(cmag)

	## psfex.xml reading
	votable=parse("psfex.xml")
	table=votable.get_first_table()
	data= table.array
	fm=data['FWHM_Mean'][0]
	fmw=data['FWHM_WCS_Mean'][0] 
	ps=data['PixelScale_WCS_Mean'][0]
	em=data['Ellipticity_Mean'][0]

	print "FWHM in pixel, ",fm, " FWHM in Arcsec, ",fmw, " pixel scale, ",ps
	print 'psfmag: ',float(smag[idx]), '  automag: ' ,float(magat[idx])
	print 'check star auto mag: ',float(cmag), ' sub= ', (float(magat[idx])-float(cmag))
	
	print 'Error= ', float(np.sqrt(smagerr[idx]**2 + val[1]**2)) 
	
	photline=files+' '+str(obsjd)+' '+"%.4f" % magat[idx]+' '+"%.4f" % magaterr +' '+"%.4f" % magap5[idx]+' '+"%.4f" % magap5err +' '+"%.4f" % magap7[idx]+' '+"%.4f" % magap7err +' '+"%.4f" % cmag +' '+"%.4f" % cdelmag+' '+"%.4f" % cdelmagrms+' '+"%.4f" % cmagerrmean+' '+"%.4f" % delmagmean+' '+"%.4f" % delmagrms+' '+ "%.0f" % apnum+' '+"%.4f" % wmean+' '+"%.4f" % werr+ ' ' +'\n'
	
	f.write(photline)	
	







f.close()



photdata=ascii.read('photresult_lcogt.txt')
#jd=photdata['jd']
#pmag=photdata['mag(psf)']
#perr=photdata['magerr']

#plt.errorbar(jd,pmag,yerr=perr)
#plt.errorbar(jd,cmag,yerr=perr)
#plt.show()

#sextractor for psfex
#psfex
#psf phot from image
#catalog matching

#zp point calculation

# all mag calibration

#object magnitude and other info, write to photresult.txt

print '\n',"ALL done."
print outfile,'\n'
