#python ds9regmake.py filename racol deccol name

import os,sys
import string
from astropy.io import ascii 
import numpy as np
import math

#filename='lcogt_match_star.cat'
#filename='craPG0934_20130407_1.cat'
filename=sys.argv[1]
racol =sys.argv[2]
deccol=sys.argv[3]
name=sys.argv[4]
data=ascii.read(filename)


#ra=data['ALPHA_J2000']
#dec=data['DELTA_J2000']
#starname=data['NUMBER']
#apermag=data[]
#automag=data['col26']
#umag=data['umag']
#gmag=data['gmag']
#nomadbmag=data['Bmag']
#sdssb=umag- 0.8116*(umag - gmag) + 0.1313

#def average(s) : return sum(s) 1.0 / len(s)

#dist=sdssb - automag
#zp=np.mean(dist)
#meanzp= sum(dist)/len(umag)
#vari=map(lamda x: (x-meanzp)**2,dist)
#std=math.sqrt(average(vari))
#stdzp=np.std(dist)
#print '%.4f' % zp ,'%.4f' % stdzp
# 26.8364 0.0918 from auto mag 
# 26.8340 0.0739 from psf mag

#sdssbmag=automag+zp

#filename='craPG0934_20130407_1.cat'
data=ascii.read(filename)


ra=data[racol]
dec=data[deccol]
starname=data[name]            # data['NUMBER']

radius=""" 10" """
color="red"
f=open(filename+'.reg','w')

head1="# Region file format: DS9 version 4.1\n"
head2="""global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n"""
head3="fk5\n"

f.write(head1)
f.write(head2)
f.write(head3)



for n in range(len(ra)):

	body="circle("+str(ra[n])+","+str(dec[n])+","+radius+") # color="+color+" text={"+str(starname[n])+"}\n"	
	f.write(body)


f.close()


