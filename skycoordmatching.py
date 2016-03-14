from astropy.coordinates import ICRS
from astropy import units as u

'''
cat1_ra = [ ra, ...]
cat1_dec = [dec, ...]
cat2_ra = [ra, ...]
cat2_dec = [dec, ...]
'''

#cat1 = ICRS(cat1_ra,cat1_dec,units = (u.degree,u.degree))
#cat2 = ICRS(cat2_ra,cat2_dec,units = (u.degree,u.degree))
cat1 = SkyCoord(cat1_ra*u.degree,cat1_dec*u.degree,frame='icrs')
cat2 = SkyCoord(cat2_ra*u.degree,cat2_dec*u.degree,frame='icrs')

index,dist2d,dist3d = cat1.match_to_catalog_sky(cat2)

for i,j in enumerate(index):
    print cat1[i], "matches with ", cat2[j], "with a separation of ",dist2d[i]
	print cat1[1].to_string(precision=1, sep=':')

#if you like hms/dms positions use
print cat1[1].to_string(precision=1, sep=':')
