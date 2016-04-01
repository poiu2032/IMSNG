#Written by Choi Changsu
#Edited by Park KeunWoo for LOAO

noao
imred
ccdred

#No dark electron

#Making image lists
ls zero.2x2.* > zero.list
ls ?f.2x2.* > flat.list
ls obj.*.fits > obj.list

#Zerocombine
zerocom @zero.list output=zero.fits combine=average reject=avsigclip ccdtype='' rdnoise=4.84 gain=2.68
#	input   =           @zero.list  List of zero level images to combine
#	(output =            zero.fits) Output zero level name
#	(combine=              average) Type of combine operation
#	(reject =            avsigclip) Type of rejection
#	(ccdtype=                     ) CCD image type to combine

#Finding vizar zero data(checking mean & stddev)
imstat zero*.fits

#Flat image - Zero(each filter could be done by one operation)
imarith @flat.list - zero.fits z@flat.list
imarith @obj.list - zero.fits d@obj.list

#Making each filter flat list
hselect @flat.list $I "FILTER  = 'R104'" > rflat.list 
hselect @flat.list $I "FILTER  = 'B102'" > bflat.list 
#hselect @flat.list $I "FILTER  = 'V103'" > vflat.list 
#hselect @flat.list $I "FILTER  = 'I105'" > iflat.list
#hselect @flat.list $I "FILTER  = 'Z'" > zflat.list 
#hselect @flat.list $I "FILTER  = 'Y'" > yflat.list 

#Flatcombine
flatcom z@rflat.list output=rflat.fits combine=median reject=avsigclip ccdtype='' process- subset- scale=mode rdnoise=4.84 gain=2.68
flatcom z@bflat.list output=bflat.fits combine=median reject=avsigclip ccdtype='' process- subset- scale=mode rdnoise=4.84 gain=2.68
#flatcom z@vflat.list output=vflat.fits combine=median reject=avsigclip ccdtype='' process- subset- scale=mode rdnoise=4.84 gain=2.68
#flatcom z@iflat.list output=iflat.fits combine=median reject=avsigclip ccdtype='' process- subset- scale=mode rdnoise=4.84 gain=2.68
#flatcom z@zflat.list output=zflat.fits combine=median reject=avsigclip ccdtype='' process- subset- scale=mode rdnoise=4.84 gain=2.68
#flatcom z@yflat.list output=yflat.fits combine=median reject=avsigclip ccdtype='' process- subset- scale=mode rdnoise=4.84 gain=2.68
#	input   =         z@rflat.list  List of flat field images to combine
#	(output =           rflat.fits) Output flat field root name
#	(combine=               median) Type of combine operation
#	(reject =            avsigclip) Type of rejection
#	(ccdtype=                     ) CCD image type to combine
#	(process=                   no) Process images before combining?
#	(subsets=                   no) Combine images by subset parameter?
#	(delete =                   no) Delete input images after combining?
#	(clobber=                   no) Clobber existing output image?
#	(scale  =                 none) Image scaling

#Finding vizar flat data
imstat z*f.2x2.*.fits

#Normalizing Flat
imstat rflat.fits field='mean' format- | scan(x)
=x
imarith rflat.fits / (x) nrflat.fits

imstat bflat.fits field='mean' format- | scan(x)
=x
imarith bflat.fits / (x) nbflat.fits

#imstat vflat.fits field='mean' format- | scan(x)
#=x
#imarith vflat.fits / (x) nvflat.fits

#imstat iflat.fits field='mean' format- | scan(x)
#=x
#imarith iflat.fits / (x) niflat.fits

#imstat zflat.fits field='mean' format- | scan(x)
#=x
#imarith zflat.fits / (x) nzflat.fits

#imstat yflat.fits field='mean' format- | scan(x)
#=x
#imarith yflat.fits / (x) nyflat.fits


#Making each filter object list
hselect @obj.list $I "FILTER  = 'R104'" > robj.list 
hselect @obj.list $I "FILTER  = 'B102'" > bobj.list  
#hselect @obj.list $I "FILTER  = 'V103'" > vobj.list 
#hselect @obj.list $I "FILTER  = 'I105'" > iobj.list 
#hselect @obj.list $I "FILTER  = 'Z'" > zobj.list 
#hselect @obj.list $I "FILTER  = 'Y'" > yobj.list 


#Final object data
imarith d@robj.list / nrflat.fits fd@robj.list
imarith d@bobj.list / nbflat.fits fd@bobj.list
#imarith d@vobj.list / nvflat.fits fd@vobj.list 
#imarith d@iobj.list / niflat.fits fd@iobj.list
#imarith d@zobj.list / nzflat.fits fd@zobj.list 
#imarith d@yobj.list / nyflat.fits fd@yobj.list 

#checking object.fits
#imstat *obj*.fits 

!ds9 -zscale fdobj*.fits -single -zoom to fit -frame match image & 
