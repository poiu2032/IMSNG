#python script for changeing value of specific keyword
#2015/05/18, Changsu
#image extention check is needed.

from astropy.io import fits
import numpy as np
import os


objfile='obj.list'

objlist=np.genfromtxt(objfile,usecols=(0),dtype=str)

#inputim='test.fits'
#keyword='FILTER'
#head[keyword] = 'R'


def change_keyval(inputim, keyword, value) :
	data=fits.getdata(inputim)
	head=fits.getheader(inputim)
	head[keyword]=value
	fits.writeto('rn'+inputim, data[0], head, clobber=True)

def chfitshead(im,key,val) :
	f=fits.open(im,mode='update')
	f[0].header[key]=val
	f.flush()
	f.close()		


for obj in objlist :
	#if fits.getheader(obj)['RA'] == 'R(Ha)' :
	chfitshead(obj,'RA','16:10:14.592')
	chfitshead(obj,'DEC','+01:03:20.50')

	#os.system('rm '+ obj)
	#os.system('mv '+'rn'+obj+' '+obj)





