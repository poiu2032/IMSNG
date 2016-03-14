# code for header edition using IRAF hedit
# USAGE : python irafhedit.py(filename, keyword, value)
# hedit('test.fits','test',dataeobs)
# for single file single keyword, single value.


from pyraf import iraf
from astropy.io import fits


def hedit(filename, keywords, value) :
	iraf.imutil()
	iraf.imutil.hedit.setParam('images',filename)
	iraf.imutil.hedit.setParam('field',keywords)
	iraf.imutil.hedit.setParam('value',value)
	iraf.imutil.hedit.setParam('add','yes')
	iraf.imutil.hedit.setParam('addonly','yes')
	iraf.imutil.hedit.setParam('verify','no')
	iraf.imutil.hedit(mode='h')

 
