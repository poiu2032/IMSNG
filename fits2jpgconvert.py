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


#infile=sys.argv[1]
#files=np.genfromtxt(infile,usecols=(0),dtype=str)
#lists=list(files)

os.system('mkdir jpg')

# Define a function for making a linear gray scale
def lingray(x, a=None, b=None):
 """
 Auxiliary function that specifies the linear gray scale.
 a and b are the cutoffs : if not specified, min and max are used
 """
 if a == None:
         a = np.min(x)
 if b == None:
         b = np.max(x)
 return 255.0 * (x-float(a))/(b-a)

# Define a function for making a logarithmic gray scale
def loggray(x, a=None, b=None):
 """
 Auxiliary function that specifies the logarithmic gray scale.
 a and b are the cutoffs : if not specified, min and max are used
 """
 if a == None:
         a = np.min(x)
 if b == None:
         b = np.max(x)          
 linval = 10.0 + 990.0 * (x-float(a))/(b-a)
 return (np.log10(linval)-1.0)*0.5 * 255.0

fwhmdata=ascii.read('fwhm.txt')

filename=fwhmdata['filename']
zp=fwhmdata['zp_auto']


def fitstojpg(image,vmin,vmax) :
	data=fits.getdata(image)
#	pl.imshow(data, cmap = mpl.cm.gray,origin='lower')
	obsdate = fits.getheader(image)['DATE-OBS']
	objname = fits.getheader(image)['OBJECT']
	vmin=np.mean(data) #100 #np.min(data)
	vmax=vmin*2 #200 #np.max(data)
	new_image_data = lingray(data)
	new_image_min = 0.
	new_image_max = np.max(new_image_data)
	pl.axis('off')
	pl.imshow(data, vmin = vmin, vmax = vmax, cmap ='gray')  
	#pl.imshow(new_image_data, vmin = vmin, vmax = vmax, cmap ='gray')  
	pl.savefig('jpg/'+image[:-5]+'.png',pad_inches=0)  

def imcopy(image)
	os.system('imcopy '+image+'[930:1330,340:640] cc'+image)



for i in range(len(filename)) :
	image='skhcre'+filename[i]		
	vmax=10**((zp[i]-26)/2.5)
	imcopy(image)	
	fitstojpg(image,0,vmax) 
	fitstojpg('cc'+image,0,vmax)


'''
for image in lists :
	fitstojpg(image)
'''


	

	
'''
	fig = aplpy.FITSFigure(image)
	fig.set_theme('pretty')               #'publication'or 'pretty'
	fig.show_colorscale(cmap='gray',stretch='linear',pmin=1,pmax=99.)
	fig.set_title(objname)
	fig.add_label(0.8,0.9,obsdate,relative=True,color='orange',weight='bold')
	fig.add_label(114.06621, -69.495733,'SN2015F',relative=False, color='yellow')
	fig.show_circles(114.06621, -69.506733,15/3600.,layer='SN2015F',color='red')	
	pl.savefig('jpg/'+image[:-5]+'.jpg')
'''

	


