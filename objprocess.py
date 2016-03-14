import os
import numpy as np

os.system('ls > date.list')

infile='date.list'
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

datelist=[]
for i in range(len(lists)) :
	if lists[i][0:3] == '201' :	datelist.append(lists[i])

os.system('mkdir com')
os.system('mkdir com/B')
os.system('mkdir com/V')
os.system('mkdir com/R')

for obsdate in datelist :
	os.chdir(obsdate)
	os.system('pwd')	
	os.system('sh ../../cos_ast.sh')
	os.chdir('..')
	mvcom='cp -r'+obsdate+' done'+obsdate
	print mvcom
	os.system(mvcom)

#os.system('cp */cCal*-R-*.fits com/R/')
#os.system('cp */cCal*-V-*.fits com/V/')
#os.system('cp */cCal*-B-*.fits com/B/')

print 'all done, check it out!'


