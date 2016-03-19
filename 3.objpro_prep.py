import os
import sys
import numpy as np

os.system('ls -d m* ngc* M* NGC* messier* IC* CGC* ic* ugc* UGC* PGC* MGC* IRAS* > direc.list')
alllist=np.genfromtxt('direc.list',usecols=(0),dtype=str)

f=open("objpro.sh",'w')	

for direc in alllist :
	com1='cd '+direc+'\n'
	f.write(com1)
	f.write('cl < /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/4.objpro.cl\n')
	#
	f.write('cd ..\n\n')

#f.write('!ds9 */fz*.fits & \n')
f.close()

os.system('pluma objpro.sh &')
#os.system('. objpro.sh')
#os.system('cat objpro.sh')
os.system('rm direc.list')
#os.system('ecl')
