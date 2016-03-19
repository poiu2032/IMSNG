noao
imred
ccdred

# Header
#SIMPLE  =                    T / conforms to FITS standard
#BITPIX  =                   16 / array data type
#NAXIS   =                    3 / number of array dimensions
#NAXIS1  =                 4096
#NAXIS2  =                 4096
#NAXIS3  =                    1
#BZERO   =                32768
#BSCALE  =                  1.0
#EXTEND  =                    T
#OBSERVAT= 'Maidanak Astronomical Observatory'
#TELESCOP= 'AZT-22 1.5m'
#OBSLAT  = '+38:40:24'
#OBSLONG = '66:53:47'
#OBSALT  = '2593m   '
#PORTNUM =                    4
#FILENAME= 'C:\obsdata\may2215_000072.fits'
#TIMESYS = 'UTC     '
#UTSTART = '23:13:45'
#UTDATE  = '2015-05-22'
#IMAGETYP= 'zero    '
#OBJECT  = 'BIAS    '
#DATASEC = '[1:4096,1:4096]'
#BIASSEC = '[4097:4196,1:4096]'
#4P_ASECD= '[1:2048,1:2048]'
#4P_BSECD= '[2149:4196,1:2048]'
#4P_CSECD= '[1:2048,2049:4096]'
#4P_DSECD= '[2149:4196,2049:4096]'
#4P_ASECB= '[2049:2098,1:2048]'
#4P_BSECB= '[2099:2148,1:2048]'
#4P_CSECB= '[2049:2098,2049:4096]'
#4P_DSECB= '[2099:2148,2049:4096]'
#CAMERAID= 'SI 620-627'
#CCDTEMP = '-108.2  '
#COMMENT
#END


# process for the one night

pwd
!gethead */*.fits FILTER OBJECT IMAGETYP EXPTIME UTDATE UTSTART RA DEC
!gethead */*.fits FILTER OBJECT IMAGETYP EXPTIME UTDATE UTSTART RA DEC > fileinfo.txt

# bias combine

cd bias
ls *.fits > zero.list
!gethead *.fits FILTER OBJECT IMAGETYP EXPTIME

zerocom @zero.list output=zero.fits combine=median reject=crreject ccdtype='' scale=none gain=1.45 rdnoise=4.7

imstat *.fits
cd ..
ls

#flat combine
cd flat
pwd

ls *.fits > flat.list
#hselect @flat.list $I "filter= 'I'" > iflat.list ; type iflat.list
hselect @flat.list $I "filter= 'R'" > rflat.list ; type rflat.list
#hselect @flat.list $I "filter= 'R(Ha)'" > raflat.list ; type raflat.list
#hselect @flat.list $I "filter= 'V'" > vflat.list ; type vflat.list
#hselect @flat.list $I "filter= 'U'" > uflat.list ; type uflat.list
hselect @flat.list $I "filter= 'B'" > bflat.list ; type bflat.list

imstat @flat.list
imarith @flat.list - ../bias/zero.fits z@flat.list
imstat z@flat.list

#flatcom z@uflat.list output=uflat.fits combine=median reject=minmax ccdtype='' process- gain=1.45 rdnoise=4.7 scale=median subset-
flatcom z@bflat.list output=bflat.fits combine=median reject=minmax ccdtype='' process- gain=1.45 rdnoise=4.7 scale=median subset-
#flatcom z@vflat.list output=vflat.fits combine=median reject=minmax ccdtype='' process- gain=1.45 rdnoise=4.7 scale=median subset-
flatcom z@rflat.list output=rflat.fits combine=median reject=minmax ccdtype='' process- gain=1.45 rdnoise=4.7 scale=median subset-
#flatcom z@iflat.list output=iflat.fits combine=median reject=minmax ccdtype='' process- gain=1.45 rdnoise=4.7 scale=median subset-
#flatcom z@raflat.list output=raflat.fits combine=median reject=minmax ccdtype='' process- gain=1.45 rdnoise=4.7 scale=median subset-

imstat *flat.fits

imstat bflat.fits field='mean' format- | scan(x)
=x
imarith bflat.fits / (x) nbflat.fits

imstat rflat.fits field='mean' format- | scan(x)
=x
imarith rflat.fits / (x) nrflat.fits


#imarith iflat.fits /  niflat.fits

#imarith raflat.fits /  nraflat.fits


imstat n*flat.fits
!ds9 n*flat.fits &
cd ..
ls

!python /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/3.objpro_prep.py

