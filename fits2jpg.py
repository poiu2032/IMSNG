#fits 2 jpg conversion
#python fits2jpg.py obj.list

import os,sys
import numpy as np
from astropy.io import fits
import pylab as pl
from astropy.io import ascii
import glob
from PIL import Image
from matplotlib import pyplot as mpl
import subprocess
import aplpy



#os.system('ls hd*.fits > fitstojpg.list')

infile=sys.argv[1]
files=np.genfromtxt(infile,usecols=(0),dtype=str)
lists=list(files)

os.system('mkdir jpg')


for image in lists :
	data=fits.getdata(image)
#	pl.imshow(data, cmap = mpl.cm.gray,origin='lower')
	obsdate = fits.getheader(image)['DATE-OBS']
	objname = fits.getheader(image)['OBJECT']
	
	
	fig = aplpy.FITSFigure(image)
	fig.set_theme('pretty')               #'publication'or 'pretty'
	fig.show_colorscale(cmap='gray',stretch='linear',pmin=1,pmax=99.)
	fig.set_title(objname)
	fig.add_label(0.8,0.9,obsdate,relative=True,color='orange',weight='bold')
	fig.add_label(114.06621, -69.495733,'SN2015F',relative=False, color='yellow')
	fig.show_circles(114.06621, -69.506733,15/3600.,layer='SN2015F',color='red')	
	pl.savefig('jpg/'+image[:-5]+'.jpg')
	

#os.system("cp  */*/Calibrate*.fit.jpg jpgtemp/")

