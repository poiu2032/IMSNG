# python code for quadrant pattern correction
# calculate value of lines near cross in the center of image
# and make them match to each other
#
#     0,4095------------4095,4095----------
#                |
#    2048    A   |  B
#       -----------------------
#    2047        |
#            D   |  C
#     0,0-----------------4095,0-----

import datetime
import astropy.io.fits as fits 
import numpy as np
import os
import sys
import robust
import glob

imlist=glob.glob('fz*.fits')
print len(imlist),'files will be processed...'
def bgscale(im) :
	print 'Quad pattern Processing of ',im,'begins...'

	head=fits.getheader(im)
	data=fits.getdata(im)

	## array slice arr[x:y]  = ( x <= index < y ) 
	## ex) range(10)[3:7] = [3, 4, 5, 6]
	## range(10) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

	aq = data[0][2048:4096,0:2048]
	bq = data[0][2048:4096,2048:4096]
	cq = data[0][0:2048,2048:4096]
	dq = data[0][0:2048,0:2048]
	print 'A', np.mean(aq)
	print 'B', np.mean(bq)
	print 'C', np.mean(cq)
	print 'D', np.mean(dq)

	av, ah=data[0][2048:4050,2047], data[0][2048,5:2045]
	bv, bh=data[0][2048:4050,2048], data[0][2048,2050:4090]

	cv, ch=data[0][40:2040,2048], data[0][2047,2050:4090]
	dv, dh=data[0][40:2040,2047], data[0][2047,5:2045]

	#np.mean(av-bv)
	#np.mean(bh-ch)
	#np.mean(ah-dh)
	#np.mean(cv-dv)

	## aa,bb,cc,dd : C and B quad is ref, because C quad has normaly the least value in bias image
	## B quad is almost similar to C quad 

	print 'offset : A - B = ' , robust.mean(av-bv)
	print 'offset : C - D = ' , robust.mean(cv-dv)

	print 'A-B, C-D difference is calculated and apply that value to both pair...'

	#aq=aq - np.mean(av-bv)
	#dq=dq + np.mean(cv-dv)

	aq=aq - (robust.mean(av)[0]-robust.mean(bv)[0])
	dq=dq + (robust.mean(cv)[0]-robust.mean(dv)[0])


	downim   = data[0][0:2048,0:4096]  ## D + C quad
	upim = data[0][2048:4096,0:4096]   ## A + B quad

	upim[0:2048,0:2048] = aq
	upim[0:2048,2048:4096] = bq
	downim[0:2048,2048:4096] = cq
	downim[0:2048,0:2048] = dq

	uplow   = upim[0,10:4085]
	downtop = downim[2047,10:4085]

	print 'Upper Half bottom line mean value = '  , robust.mean(uplow)
	print 'Lower Half top line mean value    = '  , robust.mean(downtop)
	halfdiff= robust.mean(uplow,Cut=5.0)[0] - robust.mean(downtop,Cut=5.0)[0]
	print 'difference between upper & lower region', halfdiff

	## Lower part will be reference (a little low val ~ 1-2 ADU)

	upim = upim - (robust.mean(uplow)[0] - robust.mean(downtop)[0])

	data[0][2048:4096,0:4096] = upim 
	data[0][0:2048,0:4096]    = downim

	nowdt=datetime.datetime.utcnow()
	nowdtstr=nowdt.isoformat()
	head['COMMENT'] = 'Background Scaled for Quad pattern Removal'
	head['COMMENT'] = str(nowdtstr)+' UTC'

	fits.writeto('bg'+im, data, head,clobber=True)
	print 'Back Ground Scaling for quadrant pattern is finished for ',im,'\n'

n=0
for im in imlist : 
	bgscale(im)
	n=n+1
	print n,'th file of ',len(imlist)  	
outlist=glob.glob('bgfz*.fits')
print 'from ',len(imlist),'files, ',len(outlist),'files are done.' 
print '\a'













