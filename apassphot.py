# convert APASS catalog to reference catalog for IMSNG field
# B,V (vega -> AB)
# sdss r -> johnson R
# 2015.4.20 edited
# usage : python apassphot.py inputcat outcat
# ex)     python apassphot.py apass_248.787916666667_46.2141666666667_1.csv apass_IC1222.cat
from astropy.io import ascii
import os
import sys
from astropy.io import fits
import numpy as np
import robust

#Robert Lupton 2007 conversion.
#   R = r - 0.1837*(g - r) - 0.0971;  sigma = 0.0106
#   R = r - 0.2936*(r - i) - 0.1439;  sigma = 0.0072

#vega to -> AB conversion (Frei & Gunn 1994, AJ, 108. 1476)
#V=V(AB) + 0.044 +/- 0.004
#B=B(AB) + 0.163 +/- 0.004
#R=R(AB) - 0.055 +/- INDEF 
inputcat=sys.argv[1]
apasscat    = ascii.read(inputcat,fill_values=[('NA', '-99', 'Sloan_r'),('NA', '-99', 'Sloan_i'),('NA', '-99', 'i_err'),('NA', '-99', 'r_err'),('NA', '-99', 'Johnson_V'),('NA', '-99', 'Johnson_B'),('NA', '-99', 'Sloan_g'),('NA', '-99', 'gerr'),('NA', '-99', 'B_err'),('NA', '-99', 'V_err')])

ra        = apasscat['radeg']
dec       = apasscat['decdeg']
sdssr     = apasscat['Sloan_r']
sdssrerr  = apasscat['r_err']
sdssi     = apasscat['Sloan_i']
sdssierr  = apasscat['i_err']
apassv    = apasscat['Johnson_V']
apassverr = apasscat['Verr']
apassb    = apasscat['Johnson_B']
apassberr = apasscat['B_err']
raerr     = apasscat['raerr']
decerr    = apasscat['decerr']
numberobs = apasscat['number_of_Obs']
sdssg     = apasscat['Sloan_g']
sdssgerr  = apasscat['gerr']

rconvert=[]
rerr    =[]
vab     =[]
bab     =[]
verr    =[]
berr    =[]

outcat=sys.argv[2]
f=open(outcat,'w')
colnamelist='radeg, raerr, decdeg, decerr, number_of_Obs, Johnson_V, Verr, Johnson_B, B_err, Sloan_g, gerr, Sloan_r, r_err, Sloan_i, i_err, convert_R, convert_Rerr \n'

f.write(colnamelist)

for m in range(len(sdssr)) :
	mm = sdssr[m] - 0.2936*(sdssr[m] - sdssi[m]) - 0.1439 #;  sigma = 0.0072
	rconvert.append(mm)
	vab.append(apassv[m] - 0.044)
	bab.append(apassb[m] - 0.163)
	rerr.append(np.sqrt(sdssrerr[m]**2. + sdssierr[m]**2.)) #include conversion error
	verr.append(np.sqrt(apassverr[m]**2. + 0.004**2.)) #include conversion error
	berr.append(np.sqrt(float(apassberr[m])**2. + 0.004**2.)) #include conversion error
	com="%.6f" % ra[m] +','+ "%.3f" %raerr[m] +',' + "%.6f" % dec[m] +',' + "%.3f" % decerr[m] +',' + str(numberobs[m]) +',' + "%.3f" % vab[m] +',' + "%.3f" % verr[m] +',' + "%.3f" % bab[m] +',' + "%.3f" % berr[m] +',' + "%.3f" % (sdssg[m]) +',' + "%.3f" % (sdssgerr[m]) +',' + "%.3f" % sdssr[m] +',' + "%.3f" % sdssrerr[m] +',' + "%.3f" % sdssi[m] +',' + "%.3f" % sdssierr[m] +',' + "%.3f" % rconvert[m] +',' + "%.3f" % rerr[m] +'\n'
	f.write(com)
f.close()

os.system('pluma '+outcat+' &')
print 'all done'
