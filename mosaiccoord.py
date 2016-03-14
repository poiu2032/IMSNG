# mosaic coordinate for large field with small FOV
# center coordinate of each frame calculation
# center coordinate input
# array number mx by my
# FOV size fx by fy in arcmin unit
# overlap resion size ox and oy (ox=oy, for default)
# bsize= Big picture size bx by by
# assuming field has normal direction E-left & N-up
# It will give 'name ra dec' for itelescope input coordinate
# python mosaiccoord.py 'name'      'ra'            'dec'     bx by
# python mosaiccoord.py 'NGC5139' '13:26:47.28' '-47:28:46.1' 60 60 

import astropy.units as u
from astropy.io import ascii
import ephem
import numpy as np
import string
import sys
import astropy.coordinates as coord
import astropy.units as u
import math

#center ra,dec input, name ra(hh:mm:ss) dec(dd:mm:ss) 

#name=sys.argv[1]
#ra=sys.argv[2]
#dec=sys.argv[3]
#bx=sys.argv[4]
#by=sys.argv[5]

name='NGC3586'
ra=  '11:12:39.58' 
dec= '-61:17:48.1'



rad=coord.Angle(ra,unit=u.hour)
radd=rad.degree
radh=rad.hour
decd=coord.Angle(dec,unit=u.deg)
decdd=decd.degree

#whole field size (x,y in arcmin)
bx=1.15* 60. 
by=35. 

#FOV size
fx=17.
fy=11.
#overlap region size
ox=2.
oy=2.
#scale: 0.482012 arcsec/pix
#IMAGEW  =                 2184 / Image width,  in pixels.
#IMAGEH  =                 1472 / Image height, in pixels.                       

fsize=fx * fy

ix=(bx-ox)/(fx-ox)
iy=(by-oy)/(fy-oy)


#ix=int(math.ceil( bx / (fx-ox) ))  #ra direction number
#iy=int(math.ceil( by / (fy-oy) ))  #dec direction number
print name+' Field mosaic coordinate'
print 'ra '+ra +', dec '+dec
print 'entire field is '+str(int(bx))+' x '+str(int(by))+' arcmin'
print 'To cover entire field with '+str(int(fx))+' x '+str(int(fy))+' FOV,'  
print 'x axis number', int(math.ceil(ix)), ', y axis number ', int(math.ceil(iy)), ', in total ',int(math.ceil(ix)) * int(math.ceil(iy)), ' fields are needed'

#left upper coordnate

ixhf=int(math.ceil(ix))/2
iyhf=int(math.ceil(iy))/2

segra=[]
if int(math.ceil(ix))%2 == 1 :  # odd 
	for i in range(ixhf) :
		sra = radd + ((i+1) * (fx-ox))/60.
		segra.append(sra)
	segra.append(radd)	
	for i in range(ixhf) :
		sra = radd + ((-1.)*(i+1) * (fx-ox))/60.
		segra.append(sra)
elif int(math.ceil(ix))%2 == 0 :
	for i in range(ixhf) :
		sra = radd + ((i) * (fx-ox))/60. + ((fx-ox)/2.)/60. 
		segra.append(sra)
	for i in range(ixhf) :
		sra = radd + ((-1.)*(i) * (fx-ox))/60. - ((fx-ox)/2.)/60.
		segra.append(sra)
segra.sort()

#print int(math.ceil(ix)), len(segra) ,segra

segdec=[]	

if int(math.ceil(iy))%2 == 1 :  # odd 
	for i in range(iyhf) :
		sdec = decdd + ((i+1) * (fy-oy))/60.
		segdec.append(sdec)
	segdec.append(decdd)	
	for i in range(iyhf) :
		sdec = decdd + ((-1.)*(i+1) * (fy-oy))/60.
		segdec.append(sdec)
elif int(math.ceil(iy))%2 == 0 :
	for i in range(iyhf) :
		sdec = decdd + ((i) * (fy-oy))/60. + ((fy-oy)/2.)/60. 
		segdec.append(sdec)
	for i in range(iyhf) :
		sdec = decdd + ((-1.)*(i) * (fy-oy))/60. - ((fy-oy)/2.)/60.
		segdec.append(sdec)
segdec.sort(reverse=True)

#print int(math.ceil(iy)), len(segdec) ,segdec

coordstr=[]
for dx in segra :
	for dy in segdec : 
		dxx=coord.Angle(dx,unit=u.deg)
		dyy=coord.Angle(dy,unit=u.deg)
		dxh=dxx.hour
		dyd=dyy.deg
		coordi=name+'_'+str(segra.index(dx)+1)+'-'+str(segdec.index(dy)+1)+'\t'+'%.4f' %dxh+'\t'+'%.4f' %dyd
		print name+'_'+str(segra.index(dx)+1)+'-'+str(segdec.index(dy)+1)+'\t'+'%.4f' %dxh+'\t'+'%.4f' %dyd	
		coordstr.append(coordi)
'''	
rad=coord.Angle(ra,unit=u.hour)
radd=rad.degree
radh=rad.hour
decd=coord.Angle(dec,unit=u.deg)
decdd=decd.degree
'''	
	
	
			
		
