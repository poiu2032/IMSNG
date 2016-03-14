#this code will registrate all images with names of "cCalibrate*.fits"
#be sure to have files those are comicray calibrated
#be sure to same fields
#usage : python wregister_itelescope.py

import numpy as np
import os,sys
from astropy.io import fits
from astropy.io import ascii
import astropy.units as u
import astropy.coordinates as coord
import astropy.units as u
import subprocess
from astropy.table import Table, Column
from astropy.time import Time
from pyraf import iraf
import numpy as np
import matplotlib.pyplot as plt

subprocess.call('ls cCalibrate*.fits > obj.list',shell=True)
subprocess.call('ls cCalibrate*.fits > obj.list.done',shell=True)
subprocess.call('gethead cCal*.fits DATE-OBS > obj.list.date',shell=True)
resnum=subprocess.check_output('ls cCalibrate*.fits | wc -l',shell=True)
print "files astrometry done : ", resnum
colnames=('files','obstime')

filename='obj.list.date'
info=ascii.read(filename,Reader=ascii.NoHeader,names=colnames)
info=Table(info)
info.sort('obstime')
files=info['files']
obstime=info['obstime']

objfile='obj.list.done'
objlist=np.genfromtxt(objfile,usecols=(0),dtype=str)
pathname=os.getcwd()
datestr=pathname[-8:]
targetname='IC2537'

"""
obsdt=[]
for n in range(len(files)):
	header=fits.getheader(files[n])
	hobsdate=header['DATE-OBS']
	obsdt.append(hobsdate)
print obsdt	

t = Time(obstime, format='isot', scale='utc')
tjd=t.mjd

### t format is string

tbin=[]
n=0
i=0


for n in range(len(tjd)) :
	if n==0 :
		#print n,' th file ',files[n],' in sub group : ', i  
		tbin.append([0,files[0]])
		#n=n+1
	#print tjd[n] - tjd[n-1] 	
	elif n!=len(tjd) :	
		if (n!=len(tjd)) and ((tjd[n] - tjd[n-1]) < 0.5/24.) :
			#print n,' th file ',files[n],' in sub group : ', i  
			#n=n+1
			tbin.append([i,files[n]])
	
		else : # (n!=len(tjd)) and ((tjd[n] - tjd[n-1]) >= 1/24.) :
			i=i+1		
			#print n,' th file ',files[n],' in sub group : ', i+1
			tbin.append([i,files[n]])			
			#n=n+1
			
	elif n==len(tjd) :
		#print n,' th file ',files[n],' in sub group : ', i  
		tbin.append([i,files[n]])
		break			
subnum=i
print i+1 ,' groups are generated for imcombine'

f=open('com.list','w')
for g in range(len(tbin)) :
	f.write(str(tbin[g][0])+' '+tbin[g][1]+'\n')
f.close()
os.system('cat com.list')


filename='com.list'
colnames=('sub','fname')
info1=ascii.read(filename,Reader=ascii.NoHeader,names=colnames)

info1=Table(info1)
#info1.sort('obstime')
fname=info1['fname']
sub=info1['sub']
subnum=list(set(sub))



##dictionary group
subdic={}
for subkey in subnum :

	for ii in range(len(fname)) :
		ss=np.where(sub==subkey)	
		subdic[subkey]=[fname[ss]]

gg=list(subdic.keys())

#"""
#wregister afdobj.iPTF14yb.20140227.0148.fits afdobj.iPTF14yb.20140227.0140.fits #rafdobj.iPTF14yb.20140227.0148.fits
#"""

def wregister(infile,ref,output) :
	#inlist=(",".join(inlist))
	#output=(",".join(output))
	iraf.wregister.unlearn()
	iraf.wregister.setParam('input',infile)
	iraf.wregister.setParam('output',output)
	iraf.wregister.setParam('reference',ref)
	#iraf.wregister.setParam('mode','')
	iraf.wregister(infile,ref,output)


#print gg
#inlist=[]

inlist=list(files)
for mm in range(len(inlist)) :
	output='r'+inlist[mm]
	ref="ref.fits"
	wrcom="wregister "+inlist[mm]+" "+output+" "+ref
	infile=inlist[mm]		
	print wrcom
	wregister(infile,ref,output)

		
