#catalog_radius_cut.py inradius outradious

import astropy.io.ascii as ascii
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table, Column
import numpy as np
import sys

infile='sdssdr12_NGC0337_conv_bvri.cat'
ref=ascii.read(infile)

#NGC0337 center coordinates = 14.95871 -7.57797
locx = 14.95871
locy = -7.57797

ra=ref['ra']
dec=ref['dec']

inradius=sys.argv[1]
outradius=sys.argv[2]

inradius=int(inradius)/60.
outradius=int(outradius)/60.


dist=np.sqrt((ra-locx)**2+ (dec-locy)**2)

idxsn=np.where((dist < outradius) & (dist > inradius))
print 'from the center, between',outradius*60,'and',inradius*60,'arcmin' 
print 'from',len(ra),'objects,',len(idxsn[0]), 'objects are found'

print 'creating new catalog consists of these selected objects'

ref[idxsn].write(infile[:-4]+'_'+str(int(inradius*60))+'_'+str(int(outradius*60))+'.cat',format='ascii')#, overwrite=True)

print 'output file is ',infile[:-4]+'_'+str(int(inradius*60))+'_'+str(int(outradius*60))+'.cat'
print '\a'
