#python seriesphot.py 0 phot.txt 		(0,1,2 : B,V,R)  

import os,sys
import numpy as np
from astropy.io import ascii
from astropy.io import fits
from astropy.time import Time
from astropy.io.votable import parse
from astropy.time import Time
import robust
import matplotlib.pyplot as plt


filternames=['Johnson_B','Johnson_V','convert_R']                  # B,V,R = 0,1,2 from APASS catalog
x=sys.argv[1]
x=int(x)
filtername=filternames[x]
resultfile=sys.argv[2]

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

confpath='/data0/code/'
'''
preparam = phot.param
preconfi = phot.sex
subparam = sub.param
subconfi = sub.sex
defpsfex = default.psfex
prepsfse = prepsfex.sex
prepsfpa = prepsfex.param
defswarp = default.swarp
'''

refcat='/data0/itelescope_data/t52/NGC2442/com/NGC2442_apass.new.6arcmin.cat'
refim='ref.fits'
#filename fwhm autozp autozperr	starnumber ap3zp ap3zperr ap7zp	ap7zperr ap3_auto_gap ap7_ap3_gap
inimlist      = ascii.read('fwhm'+filtername+'.txt')
inim          = inimlist['filename']
fwhm          = inimlist['fwhm']
autozp        = inimlist['autozp']
autozperr     = inimlist['autozperr']
ap3zp         = inimlist['ap3zp'] 
ap3zperr      = inimlist['ap3zperr']
ap7zp         = inimlist['ap7zp']
ap7zperr      = inimlist['ap7zperr']
ap3_auto_gap  = inimlist['ap3_auto_gap']
ap7_ap3_gap   = inimlist['ap7_ap3_gap'] 

starnum  = inimlist['starnumber']


os.system('gethead sub*.fits DATE-OBS filter exptime  > headinfo.txt')

'''
error < 0.01
flag == 0
0.8 < stellarity < 1 
fwhm = []
zp   = []
zperr= []
os.system("cp /data0/code/psfex.config/* .")
'''

#extinction=0.735  # B
#extinction=0.556  # V
#extinction=0.440  # R

apersize='3,5,7,9,11,13,15,17,19,21'
detecthred = '1.2'
analthred  = '1.2'

#subtracted image photometry

snra  = 114.0661043 
sndec = -69.5068077
snmag, snapmag3 ,snapmag7,snap3cor7             = [],[],[],[]
snmagerr,snapmagerr3, snapmagerr7 ,snap3cor7err = [],[],[],[]
idx                               = []

for i in range(len(inim)-1) :
	inimage='sub'+inim[i]
	presecom="sex -c prepsfex.sex "+inimage+" -CATALOG_NAME "+inimage[:-5]+".cat"
	psfexcom="psfex -c default.psfex "+inimage[:-5]+".cat"
	os.system(presecom)
	os.system(psfexcom)
	sexcom='sex -c ../phot.sex '+inimage+' -CATALOG_NAME '+inimage[:-5]+'.cat -PARAMETERS_NAME  ../phot.param -psf_name '+inim[i][:-5]+'.psf -seeing_fwhm '+str(list(fwhm)[i])+' -DETECT_THRESH '+detecthred+' -ANALYSIS_THRESH '+analthred+' -PHOT_APERTURES '+apersize 
	os.system(sexcom)
	cat=ascii.read(inimage[:-5]+'.cat',delimiter=' ')
	
	sra         = cat['col4'] 
	sdec        = cat['col5']
	automag     = cat['col8']
	automagerr  = cat['col9']
	apmag3      = cat['col44']
	apmagerr3   = cat['col54']
	apmag7      = cat['col48']
	apmagerr7   = cat['col58']

#	sra = list(cat['ALPHA_J2000'])
#	sdec= list(cat['DELTA_J2000'])	
#	automag=cat['MAG_AUTO']
#	automagerr=cat['MAGERR_AUTO']

	dist=(np.sqrt((sra-snra)**2+ (sdec-sndec)**2))
	idx=np.where((dist < (3/3600.)) & (dist==min(dist)))
	if	list(idx[0])==[] :
		snmag.append(99.)
		snapmag3.append(99.)
		snapmag7.append(99.)
		snap3cor7.append(99.)
		snmagerr.append(99.)
		snapmagerr3.append(99.)
		snapmagerr7.append(99.)
		snap3cor7err.append(99.)


	else : 
		snmag.append((automag[idx]+autozp[i])[0]  )#- extinction)
		snapmag3.append((apmag3[idx]+ap3zp[i])[0] )
		snapmag7.append((apmag7[idx]+ap7zp[i])[0] )
		snap3cor7.append((apmag3[idx]+ap3zp[i]-ap7_ap3_gap[i])[0] )		

		snmagerr.append(    (np.sqrt(automagerr[idx]**2 + autozperr[i]**2))[0])
		snapmagerr3.append( (np.sqrt(apmagerr3[idx]**2  +  ap3zperr[i]**2))[0])
		snapmagerr7.append( (np.sqrt(apmagerr7[idx]**2  +  ap7zperr[i]**2))[0])
		snap3cor7err.append((np.sqrt(apmagerr3[idx]**2  +  ap3zperr[i]**2))[0])

	print inim[i],'%.3f' %snmag[i],'%.3f' %snmagerr[i],'%.3f' %snapmag3[i],'%.3f' %snapmagerr3[i],'%.3f' %snapmag7[i],'%.3f' %snapmagerr7[i],'%.3f' %snap3cor7[i], '%.3f' %snap3cor7err[i]





k=open(resultfile,'w')
tt=[]
for i in range(len(inim)-1) :
	inimage = inim[i]
	head    = fits.getheader(inimage)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)
	print tjd,snmag[i],snmagerr[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
	#comment = str(tjd)+'\t'+str(list(snmag[i]))+'\t'+str(list(snmagerr[i]))+'\n'
	comment = inimage+'\t'+obsdate+'\t'+'%.7f' % tjd+'\t'+'%.3f' % snmag[i]+'\t'+'%.3f' %snapmagerr3[i]+'\t'+'%.3f' %snapmag7[i]+'\t'+'%.3f' %snapmagerr7[i]+'\t'+'%.3f' %snap3cor7[i]+'\t'+ '%.3f' %snap3cor7err[i]+'\n'
	k.write(comment)

k.close()

k=open('snpy_aper3'+resultfile,'w')
tt=[]
for i in range(len(inim)-1) :
	inimage = inim[i]
	head    = fits.getheader(inimage)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)
	print tjd,snapmag3[i],snapmagerr3[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
	#comment = str(tjd)+'\t'+str(list(snmag[i]))+'\t'+str(list(snmagerr[i]))+'\n'
	comment = '%.7f' %(tjd)+'\t'+'%.3f' % (snapmag3[i])+'\t'+'%.3f' %(snapmagerr3[i])+'\n'
	k.write(comment)

k.close()

k=open('snpy_aper7'+resultfile,'w')
tt=[]
for i in range(len(inim)-1) :
	inimage = inim[i]
	head    = fits.getheader(inimage)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)
	print tjd,snapmag7[i],snapmagerr7[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
	comment = '%.7f' %(tjd)+'\t'+'%.3f' % (snapmag7[i])+'\t'+'%.3f' %(snapmagerr7[i])+'\n'
	k.write(comment)

k.close()

k=open('snpy_aper3cor7'+resultfile,'w')
tt=[]
for i in range(len(inim)-1) :
	inimage = inim[i]
	head    = fits.getheader(inimage)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)
	print tjd,snap3cor7[i],snap3cor7err[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
	comment = '%.7f' %(tjd)+'\t'+'%.3f' % (snap3cor7[i])+'\t'+'%.3f' %(snap3cor7err[i])+'\n'
	k.write(comment)

k.close()


k=open('snpy_auto'+resultfile,'w')
tt=[]
for i in range(len(inim)-1) :
	inimage = inim[i]
	head    = fits.getheader(inimage)
	obsdate = head['DATE-OBS']
	t       = Time(obsdate, format='isot', scale='utc')
	tjd     = t.mjd
	tt.append(tjd)
	print tjd,snmag[i],snmagerr[i]             #inimage,obsdate,tjd,list(snmag[i]),list(snmagerr[i])
	#comment = str(tjd)+'\t'+str(list(snmag[i]))+'\t'+str(list(snmagerr[i]))+'\n'
	comment = '%.7f' %(tjd)+'\t'+'%.3f' % (snmag[i])+'\t'+'%.3f' %(snmagerr[i])+'\n'
	k.write(comment)

k.close()


print 'all done'
os.system('pluma '+resultfile+' snpy*'+resultfile+' &')
'''

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(tt,snmag, marker='.',color='b',s=5)
#ax.set_xlim(,12000)
#ax.set_ylim(2,4)
ax.grid(True)
ax.set_title('Light curve of NGC2442 in B band')
ax.set_xlabel('MJD')
ax.set_ylabel('MAG NOMAD catalog calibrated')

fig.savefig("lc_B.pdf")


'''




