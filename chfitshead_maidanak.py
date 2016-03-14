#python script for changeing value of specific keyword
#2015/05/18, Changsu
#image extention check is needed.

from astropy.io import fits
from astropy.io import ascii
import numpy as np
import os

os.system("ls ctbgfz*.fits > obj.list")
objfile='obj.list'

#input1= 'IC1222'           #OBJECT NAME
#input2= '16:35:09.096'     #RA
#input3= '+46:12:51.01'     #DEC

tt=ascii.read('../../alltarget.dat')

dirhere = os.getcwd()
dirhere = dirhere.split('/') 
pwd=dirhere[-1]
num=np.where(pwd==tt['obj'])
tt['obj'][num][0]

input1,input2,input3 = 'IC1222',		'16:35:09.096',		'+46:12:51.01'#CGCG023-019'		,'16:10:14.592'		,'+01:03:20.50'

input1,input2,input3 = tt['obj'][num][0],tt['ra'][num][0],tt['dec'][num][0]

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
	utstart,utdate=f[0].header['UTSTART'],f[0].header['UTDATE']
	dateobs=utdate+'T'+utstart
	f[0].header['DATE-OBS']=dateobs
	print 'DATE-OBS is updated to', dateobs
	f.flush()
	f.close()		

n=0
for obj in objlist :
	#if fits.getheader(obj)['RA'] == 'R(Ha)' :
	n=n+1
	print n,'th file of ',len(objlist)  	
	chfitshead(obj,'OBJECT',input1)
	chfitshead(obj,'RA',input2)
	chfitshead(obj,'DEC',input3)
	print 'Inputs are', input1, input2, input3
	print 'header is changed', fits.getheader(obj)['OBJECT'], fits.getheader(obj)['RA'],fits.getheader(obj)['DEC']

	#os.system('rm '+ obj)
	#os.system('mv '+'rn'+obj+' '+obj)





