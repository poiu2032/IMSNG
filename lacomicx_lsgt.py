import os
import sys
from astropy.io import fits
import lacosmicx

inim='test.fits'

indat=fits.getdata(inim)
inhdr=fits.getheader(inim)

#maskdat,outdat=lacosmicx.lacosmicx(indat, inmask=None, sigclip=4.5, sigfrac=0.3, objlim=5.0, gain=1.0, readnoise=6.5, satlevel=65536.0, pssl=0.0, niter=4)
 #, sepmed=True, cleantype='meanmask', fsmode='median', psfmodel='gauss', psffwhm=2.5,psfsize=7, psfk=None, psfbeta=4.765, verbose=False)

maskdat,outdat=lacosmicx.lacosmicx(indat, sigclip=5, sigfrac=0.3, objlim=5.0, gain=1.38, readnoise=10, niter=4,satlevel=50000.0, fsmode='median',sepmed=False, verbose=True)

outname='c'+inim

fits.writeto(outname,outdat,inhdr,clobber=True)


