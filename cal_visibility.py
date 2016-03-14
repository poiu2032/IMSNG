#cal_visibility.py
#calculate rise transit set time and moon distance

import mskpy.observing as obs
#from mskpy import Earth, Moon
import astropy.units as u
from astropy.io import ascii
import ephem
from numpy import *
import string
import sys
import astropy.coordinates as coord


#obsdate='2014/11/27'
obsdate=raw_input('obsdate?  input in format of 2014/11/30 : ')
#observatory=raw_input('observatory name?  :  ')

dts='0'
dts=raw_input('daytimesaving for observatory? input 1 for true or 0 for false ')
if dts=='0':
	print 'No day Time saving'
else:
	print 'Ok then I will plus 1 hr to local time.'
	dts=float(dts)

obsinfo=ascii.read("obscoord.txt")
#obsname=obsinfo['name']
obslat=obsinfo['latitude(N+)']
obslon=obsinfo['longitude(E+)']
obstz=obsinfo['timezone']

catname="nuvtest.dat"
tdata=ascii.read(catname)

mcoord=ephem.Moon()
mcoord.compute(obsdate)
objname=tdata['obj']
ra=tdata['ra']
dec=tdata['dec']


rad=coord.Angle(ra,unit=u.hour)
radd=rad.degree
decd=coord.Angle(dec,unit=u.deg)
decdd=decd.degree

print 'Moon ra, dec \n'
mheader='Moon ra, dec'
print mcoord.ra,mcoord.dec,'\n'
minfo=mheader+ ' '+str(mcoord.ra)+' '+str(mcoord.dec)+'\n'
mphase=ephem.Moon(obsdate+' 00:00:00')
print 'Moon phase : '+ "%.2f" % mphase.moon_phase
mphasestr='Moon phase : '+ "%.2f" % mphase.moon_phase +'\n'

def angsep(ra1deg,dec1deg,ra2deg,dec2deg):
    """ Determine separation in degrees between two celestial objects 
        arguments are RA and Dec in decimal degrees. 
    """
    ra1rad=ra1deg*pi/180
    dec1rad=dec1deg*pi/180
    ra2rad=ra2deg*pi/180
    dec2rad=dec2deg*pi/180
    
    # calculate scalar product for determination
    # of angular separation
    
    x=cos(ra1rad)*cos(dec1rad)*cos(ra2rad)*cos(dec2rad)
    y=sin(ra1rad)*cos(dec1rad)*sin(ra2rad)*cos(dec2rad)
    z=sin(dec1rad)*sin(dec2rad)
    
    rad=arccos(x+y+z) # Sometimes gives warnings when coords match
    
    # use Pythargoras approximation if rad < 1 arcsec
    sep = choose( rad<0.000004848 , (
        sqrt((cos(dec1rad)*(ra1rad-ra2rad))**2+(dec1rad-dec2rad)**2),rad))
        
    # Angular separation
    sep=sep*180/pi

    return sep

targets=[]
targets.append(rad)
targets.append(decd)
targets.append(objname)
msep=angsep(radd,decdd,mcoord.ra, mcoord.dec)
#rtscal=obs.rts(radd, decdd, obsdate, obslon, obslat, '-10', limit=20, precision=1440)


#obsdate='2014/12/30'
observ=ephem.Observer()
observ.date=obsdate+' 01:00:00'
observ.lon=str(obslon[3])
observ.lat=str(obslat[3])
observ.horizon='-18'
#sunrise=observ.previous_rising(ephem.Sun())
sunrise=observ.next_rising(ephem.Sun())
#sunset1=observ.next_setting(ephem.Sun())
sunset=observ.previous_setting(ephem.Sun())
#print('sunrise : %s' % sunrise)

aaa=ephem.Date.tuple(sunset)
hrr=aaa[3]+obstz[3]+dts
mrr=aaa[4]
print 'sunset : '+str(hrr)+':'+str(mrr)
sunsetstr='-18 deg sunset : '+str(int(hrr))+':'+str(mrr)+'\n'
sunseti=hrr + mrr/60. + 0.5

bbb=ephem.Date.tuple(sunrise)
hrr=bbb[3]+obstz[3]+dts-24
mrr=bbb[4]
print 'sunrise : '+str(int(hrr))+':'+str(mrr)
sunrisestr='-18 deg sunrise : '+str(int(hrr))+':'+str(mrr)+'\n'
sunriseti=hrr + mrr/60. -0.5
#aaa=ephem.Date.tuple(sunset1)
#hrr=aaa[3]+11
#mrr=aaa[4]
 
 
f=open("rts_vis_"+obsdate[0:4]+obsdate[5:7]+obsdate[8:10]+".txt",'w')
header='name ra dec rise(LT) transit(LT) set(LT) moon_dist(deg) \n'
dashline='------------------------------------------------------- \n'
f.write(obsdate)
f.write('\nobservatory = SSO \n')
f.write(sunsetstr)
f.write(sunrisestr)

f.write(minfo)
f.write(mphasestr)
f.write(dashline)
f.write(header)
#f.write(dashline)
#f.write('\n')

pobj=[]
prt=[]
ptt=[]
pst=[]

for n in range(len(rad)):
	
	rtscal=obs.rts(radd[n], decdd[n], obsdate, obslon[3], obslat[3], float(obstz[3])+dts, limit=35, precision=1440)
	rt=rtscal[0]
	tt=rtscal[1]
	st=rtscal[2]
	
	if rtscal[0]==None:
		print objname[n],ra[n],dec[n], rtscal[0], rtscal[1], rtscal[2],"%.2f" % msep[n]
		vis=objname[n]+' '+ra[n]+' '+dec[n]+ ' '+str(rtscal[0])+' '+ str(rtscal[1])+' '+ str(rtscal[2])+' '+str(int(msep[n]))+'\n'	
		#f.write(vis)
	
	elif sunriseti < rtscal[0] < sunseti and sunriseti < rtscal[2] < sunseti and sunriseti < rtscal[1] < sunseti : 
		print 'It can be seen in daytime!'
	elif msep[n] < 30 :
		print objname[n]+' too close to Moon <30 deg'

	else:
		rtp=repr(int(rt))+':'+repr(int((rt-int(rt))*60))
		ttp=repr(int(tt))+':'+repr(int((tt-int(tt))*60))
		stp=repr(int(st))+':'+repr(int((st-int(st))*60))
		vis=objname[n]+' '+ra[n]+' '+dec[n]+ ' '+rtp+' '+ttp+' '+stp+' '+str(int(msep[n]))+'\n'
		f.write(vis)
		print objname[n],ra[n],dec[n], rtp,ttp,stp,"%.2f" % msep[n]
		
f.close()

# plot part is undergoing!!!


#from mskpy import observing
#import astropy.units as u
import matplotlib.pyplot as plt
targets = obs.file2targets('test.data')
telescope = obs.Observer(obslon[3]	* u.deg, obslat[3] * u.deg, dts+obstz[3],obsdate, 'SSO')
obs.am_plot(targets, telescope)
plt.show()







#''''
#import staralt
#from datetime import date
#s = staralt.StarAlt()
#s = staralt.StarAlt.staralt()
#s.mode = "staralt"

#s.date = date(int(obsdate[0:4]),int(obsdate[5:7]),int(obsdate[8:10]))
#s.coordinates = [
#    staralt.coordinate(name=targetinput['col1'], ra=targetinput['col2'], #dec=targetinput['col3']),
#    ]
#s.moon_distance = True                  # Defaults to True
#s.min_elevation = 30                    # Defaults to 30

#s.save_image("image.gif")
#'''
