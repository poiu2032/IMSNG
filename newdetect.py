### com/

import os
import sys

cdir=os.getcwd()
dircut=cdir.split('/')
obj=dircut[4]
os.system('mv *-B-*.fits B/') 
os.system('mv *-V-*.fits V/') 
os.chdir('R')

try : 
	os.mkdir('old')
	
except : print 'moving files ...'

os.system('mv *cCalibrate* old/')
os.system('mv ../*-R-*.fits .')

os.system('python /data0/code/mypy/remap_lsgt.py')
os.system('python /data0/code/mypy/imagecombine_lsgt.py')
os.system('python /data0/code/mypy/fwhmzp_apass_lsgt_2nd.py convert_R '+'../apass_'+obj+'.cat')
os.system('python /data0/code/mypy/hotpantsrun_lsgt.py')	 
os.system('python /data0/code/mypy/detect_lsgt.py')

print 'Done'
print 'Go to jpg directory and check files'

'''
mv *-B-*.fits B/
mv *-V-*.fits V/
cd R
mkdir old
mv *cCalibrate* old/
mv ../*-R-*.fits .
python /data0/code/mypy/remap_lsgt.py
python /data0/code/mypy/imagecombine_lsgt.py
python /data0/code/mypy/fwhmzp_apass_lsgt_2nd.py convert_R ../apass_NGC6902.cat
python /data0/code/mypy/hotpantsrun_lsgt.py	 
python /data0/code/mypy/detect_lsgt.py
'''


