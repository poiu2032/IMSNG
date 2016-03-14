# sextracted catalog should have two keywords
#ra=data['ALPHA_J2000']
#dec=data['DELTA_J2000']

import string
from astropy.io import ascii 
import numpy as np
import math

filename=raw_input('filename: ')
#filename='craPG0934_20130407_1.cat'
data=ascii.read(filename)


ra =data['col4']
dec=data['col5']
starname=data['col1']

radius=""" 10" """
color="yellow"
f=open(filename[:-5]+'.reg','w')

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


