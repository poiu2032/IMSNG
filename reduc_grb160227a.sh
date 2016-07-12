#made by sylee

noao
imred
ccdred

hselect *.fits $I "OBJECT = 'Domeflat'" > df.list
hselect *.fits $I "OBJECT = 'Skyflat'" > sf.list
hselect @df.list $I "FILTER = 'R'" > rdf.list
hselect @sf.list $I "FILTER = 'R'" > rsf.list

hselect *.fits $I "OBJECT = 'bias'" > bias.list
hselect *.fits $I "OBJECT = 'GRB160227A'" > obj.list
hselect @obj.list $I "FILTER = 'R'" > robj.list

#zero
zerocomb @bias.list output=zero.fits combine=average reject=avsigclip ccdtype='' rdnoise=8.2 gain=1.2

imstat @bias.list
imstat zero.fits


#images -zero
imarith @rdf.list - zero.fits z@rdf.list
imarith @rsf.list - zero.fits z@rsf.list
imarith @robj.list - zero.fits z@obj.list



#flat
flatcomb z@rdf.list output=rdflat.fits combine=median reject=avsigclip ccdtype="" process- subset- scale=mode rdnoise=8.2 gain=1.2
flatcomb z@rsf.list output=rsflat.fits combine=median reject=avsigclip ccdtype="" process- subset- scale=mode rdnoise=8.2 gain=1.2

imstat @rdf.list
imstat @rsf.list
imstat rdflat.fits
imstat rsflat.fits

#nomalization
imstat rdflat.fits field='mean' format- | scan(x)
=x
imarith rdflat.fits / (x) nrdflat.fits

imstat rsflat.fits field='mean' format- | scan(y)
=y
imarith rsflat.fits / (y) nrsflat.fits

#image -flat
imarith z@robj.list / nrdflat.fits fdz@robj.list
imarith z@robj.list / nrsflat.fits fsz@robj.list 
