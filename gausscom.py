from astropy.io import ascii
import numpy as np
import os
from astropy.io import fits
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u

infile='obj.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)
fname=lists
fwhm= [ 5.2118001, 7.3981099,  4.9474101,  4.8689499,  5.0117602,  5.9481702,  5.1940899,  5.2536802]

fwhmmax=max(fwhm)
print 'max= ',fwhmmax
#n=n_elements(nstar)[5.8621302,


#fwhmk=fwhm0[where(ifilter eq 4)]
#fwhmh=fwhm0[where(ifilter eq 3)]
#fwhmj=fwhm0[where(ifilter eq 2)]
#fwhmy=fwhm0[where(ifilter eq 1)]
#fwhmz=fwhm0[where(ifilter eq 0)]

#fwhm_max=max(fwhm)
#;fwhm_max=3.0/0.2
#;fwhm_max=5.5
fwhm_max=max(fwhm)



f=open('gausscom.cl','w')

for n in range(len(fwhm)) :

	sig0=fwhm[n]/2.35
	sig05=(fwhm_max/2.35)**2. - sig0**2.

	fname_in=fname[n]
	fname_out='convr'+fname[n]

	if sig05 > 0. :

		sig=np.sqrt(sig05)
		sig_st=str(sig)#,format='(f4.2)')

		st='gauss ' + fname_in + ' ' + fname_out + ' sigma=' + sig_st + '\n'

	else : 

		st='imcopy ' + fname_in + ' ' + fname_out + '\n'

	subcom='imarith '+fname_in+' - '+fname_out+ ' sub'+fname_in +'\n' 
		
	f.write(st)
	f.write(subcom)


f.close()

 
