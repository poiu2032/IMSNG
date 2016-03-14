import numpy as np
from astropy.io import fits
from astropy.io import ascii
import os
import sys
from pyraf import iraf

#file list and information
os.system('rename \'fit\' \'fits\' *.fit')
os.system('ls *.fits > all.list')
os.system('gethead *.fits IMAGETYP OBJECT EXPTIME DATE-OBS> fileinfo.txt')

fileinfo=ascii.read('fileinfo.txt')
print fileinfo

os.system('ls bias*.fits > bias.list')
os.system('ls dark*.fits > dark.list')
os.system('ls flat*.fits > flat.list')
os.system('ls flat*B.fits > bflat.list')
os.system('ls flat*V.fits > vflat.list')
os.system('ls flat*R.fits > rflat.list')

# different data moving
#NPIX=4194304

alllist=np.genfromtxt('all.list',usecols=(0),dtype=str)
alllist=fileinfo['col1']
biaslist=[]
darklist=[]
flatlist=[]
objlist=[]
rflatlist=[]
bflatlist=[]
robjlist=[]
bobjlist=[]
for files in alllist : 
	if files[0:4]== 'bias' : biaslist.append(files)		
	elif files[0:4]== 'dark' : darklist.append(files)
	elif files[0:4]== 'flat' : flatlist.append(files)	
	else : objlist.append(files)

print 'BIAS',biaslist
print 'DARK',darklist
print 'FLAT',flatlist
print 'OBJECT',objlist

for files in flatlist : 
	if files[-6] == 'R' : rflatlist.append(files)
	elif files[-6] == 'B' : bflatlist.append(files)

for files in objlist : 
	if files[-6] == 'R' : robjlist.append(files)
	elif files[-6] == 'B' : bobjlist.append(files)

def imstat(inlist) :
	inlist=(",".join(inlist))
	iraf.imstat.setParam('images',inlist)
	iraf.imstat(inlist)


f=open("bflat.list",'w')
for files in bflatlist : 
	com=files+'\n'	
	f.write(com)
f.close()

f=open("rflat.list",'w')
for files in rflatlist : 
	com=files+'\n'	
	f.write(com)
f.close()

f=open("obj.list",'w')
for files in objlist : 
	com=files+'\n'	
	f.write(com)
f.close()

f=open("robj.list",'w')
for files in robjlist : 
	com=files+'\n'	
	f.write(com)
f.close()

f=open("bobj.list",'w')
for files in bobjlist : 
	com=files+'\n'	
	f.write(com)
f.close()

