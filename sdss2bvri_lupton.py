import astropy.io.ascii as ascii
import os
import sys
from astropy.table import Table,Column

sdss = Table.read('sdssdr12_NGC0337a.fits') # downloaded from cas.sdss.org as fits format

#sdss=ascii.read('sdssdr12_NGC0337a.fits')
sdss.colnames
'''
catalog from DS9 downloaded result
sdss.remove_column('zsp')
sdss.remove_column('mode')
sdss.remove_column('q_mode')
sdss.remove_column('cl')
sdss.remove_column('Im')
sdss.remove_column('m_SDSS9')
sdss.remove_column('Q')
'''
gmag,rmag,imag = sdss['g'],sdss['r'],sdss['i']
gerr, rerr, ierr = sdss['Err_g'],sdss['Err_r'],sdss['Err_i']

#mag conversion
#Robert Lupton 2007 conversion.
#   R = r - 0.1837*(g - r) - 0.0971;  sigma = 0.0106
#   R = r - 0.2936*(r - i) - 0.1439;  sigma = 0.0072
#	I = r - 1.2444*(r - i) - 0.3820;  sigma = 0.0078

'''
Stars
* used equation.(gri based, low sigma first)

   B = u - 0.8116*(u - g) + 0.1313;  sigma = 0.0095
   *B = g + 0.3130*(g - r) + 0.2271;  sigma = 0.0107
Bmag = gmag + 0.3130*(gmag - rmag) + 0.2271	# sigma = 0.0107
   V = g - 0.2906*(u - g) + 0.0885;  sigma = 0.0129
   *V = g - 0.5784*(g - r) - 0.0038;  sigma = 0.0054
Vmag = gmag - 0.5784*(gmag - rmag) - 0.0038 # sigma = 0.0054
   R = r - 0.1837*(g - r) - 0.0971;  sigma = 0.0106
   *R = r - 0.2936*(r - i) - 0.1439;  sigma = 0.0072
Rmag = rmag - 0.2936*(rmag - imag) - 0.1439 # sigma = 0.0072
   *I = r - 1.2444*(r - i) - 0.3820;  sigma = 0.0078
   I = i - 0.3780*(i - z)  -0.3974;  sigma = 0.0063
Imag = rmag - 1.2444*(rmag - imag) - 0.3820 # sigma = 0.0078

'''
'''
#vega to -> AB conversion (Frei & Gunn 1994, AJ, 108. 1476)
#V=V(AB) + 0.044 +/- 0.004
#B=B(AB) + 0.163 +/- 0.004
#R=R(AB) - 0.055 +/- INDEF 
 Conversion from AB magnitudes to Johnson magnitudes:
    The following formulae convert between the AB magnitude systems and those based on Alpha Lyra:

        * V	=   V(AB) + 0.044	(+/- 0.004)
        * B	=   B(AB) + 0.163	(+/- 0.004)
        Bj	=  Bj(AB) + 0.139	(+/- INDEF)
        * R	=   R(AB) - 0.055	(+/- INDEF)
        * I	=   I(AB) - 0.309	(+/- INDEF)
         g	=   g(AB) + 0.013	(+/- 0.002)
         r	=   r(AB) + 0.226	(+/- 0.003)
         i	=   i(AB) + 0.296	(+/- 0.005)
         u'	=  u'(AB) + 0.0	        
         g'	=  g'(AB) + 0.0	        
         r'	=  r'(AB) + 0.0	        
         i'	=  i'(AB) + 0.0	        
         z'	=  z'(AB) + 0.0	        
        Rc	=  Rc(AB) - 0.117	(+/- 0.006)
        Ic	=  Ic(AB) - 0.342	(+/- 0.008)

    Source: Frei & Gunn 1994, AJ, 108, 1476 (their Table 2). 
'''
Bmag = gmag + 0.3130*(gmag - rmag) + 0.2271	# sigma = 0.0107
Berr = np.sqrt(gerr**2 + 0.3130*(rerr**2+gerr**2) + 0.0107**2) 

Vmag = gmag - 0.5784*(gmag - rmag) - 0.0038 # sigma = 0.0054
Verr = np.sqrt(gerr**2 + 0.5784*(gerr**2+rerr**2) + 0.0054**2)

Rmag = rmag - 0.2936*(rmag - imag) - 0.1439 # sigma = 0.0072
Rerr = np.sqrt(rerr**2 + 0.2936*(rerr**2+ierr**2) + 0.0072**2)

Imag = rmag - 1.2444*(rmag - imag) - 0.3820 # sigma = 0.0078
Ierr = np.sqrt(rerr**2 + 1.2444*(rerr**2+ierr**2) + 0.0078**2)

'''
convmag=[]
for i in range(len(sdss['gmag'])) :
	if i==0 : tmpmag=0
	tmpmag=sdss['gmag'][i]+ 0.3130*(sdss['gmag'][i]-sdss['rmag'][i]) + 0.2271
	convmag.append(bmag)
'''
Bm = Column(name='Bmag', data=Bmag)
Be = Column(name='Berr', data=Berr)
Vm = Column(name='Vmag', data=Vmag)
Ve = Column(name='Verr', data=Verr)
Rm = Column(name='Rmag', data=Rmag)
Re = Column(name='Rerr', data=Rerr)
Im = Column(name='Imag', data=Imag)
Ie = Column(name='Ierr', data=Ierr)

sdss.add_column(Bm)
sdss.add_columns([Be,Vm])
sdss.add_columns([Ve,Rm,Re,Im,Ie])

sdss.write('sdssdr12_NGC0337_conv_bvri.cat', format='ascii')
print '\a'
print 'check the output file' 



