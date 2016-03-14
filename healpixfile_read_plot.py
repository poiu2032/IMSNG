import healpy as hp
import matplotlib.pyplot as plt
import astropy.table as tbl
import astropy.coordinates as coord
import astropy.units as u
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt


fig1 = plt.figure(figsize=(16,12))
fig = plt.figure(figsize=(16,12))
ax1 = fig1.add_subplot(111, projection="mollweide")

map=hp.read_map('bayestar.fits')
ax1=hp.mollview(map, fig=1, coord=['C','C'],title='Transient and IMSNG targets')
hp.graticule(ax1)


imsngcat='/data0/IMSNG/target/alltarget.dat'
data=ascii.read(imsngcat)

ra = coord.Angle(data['ra'],unit=u.hour)
ra = ra.wrap_at(180*u.degree)
dec = coord.Angle(data['dec'],unit=u.deg)
name =data['obj']
#fig1 = plt.figure(figsize=(8,6))
#ax = fig.add_subplot(111, projection="mollweide")
#ax.scatter(ra.radian, dec.radian)

ind1=np.where(data['priority']==1)
ind2=np.where(data['priority']==2)

ra1= ra[ind1]
dec1=dec[ind1]
ra2= ra[ind2]
dec2=dec[ind2]
name1=name[ind1]
name2=name[ind2]

#mollweide projection
ax1.scatter(ra1.radian, dec1.radian,marker='o',color='r')
ax1.scatter(ra2.radian, dec2.radian,marker='s',color='b')
k=0
for k in range(len(ra2)) : ax1.text(ra2.radian[k], dec2.radian[k], name2[k])
k=0
for k in range(len(ra1)) : ax1.text(ra1.radian[k], dec1.radian[k], name1[k])

ax1.set_xticklabels(['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h'])
#ax1.set_yticklabels(['-90d','-60d','-30d','0','30d','60d','90d'])
ax1.grid(True)
ax1.set_title('Target distribution on sky (RA, Dec)')
ax1.set_xlabel('RA')
ax1.set_ylabel('DEC')
ax1.legend(('M nuv > -18.4 , D < 50 Mpc', 'M nuv > -19.0 , D < 300 Mpc'),loc='lower center')




plt.show()
