#made by sylee

noao
imred
ccdred

cp /home/sylee/Desktop/obs_cos/red/calibration/20160411/Bias.fit ./
cp /home/sylee/Desktop/obs_cos/red/calibration/20160411/Dark.fit ./


ls T52*-B-*.fit > B.list
ls T52*-V-*.fit > V.list
ls T52*-R-*.fit > R.list
ls T52*-I-*.fit > I.list


#images -zero
imarith @B.list - Bias.fit z@B.list
imarith @V.list - Bias.fit z@V.list
imarith @R.list - Bias.fit z@R.list
imarith @I.list - Bias.fit z@I.list

imarith z@B.list - Dark.fit dz@B.list
imarith z@V.list - Dark.fit dz@V.list
imarith z@R.list - Dark.fit dz@R.list
imarith z@I.list - Dark.fit dz@I.list


#flat
#nomalization
imstat *_flat-B.fit field='mean' format- | scan(x)
=x
imarith *_flat-B.fit / (x) nBflat.fits

imstat *_flat-V.fit field='mean' format- | scan(x)
=x
imarith *_flat-V.fit / (x) nVflat.fits

imstat *_flat-R.fit field='mean' format- | scan(x)
=x
imarith *_flat-R.fit / (x) nRflat.fits

imstat *_flat-I.fit field='mean' format- | scan(x)
=x
imarith *_flat-I.fit / (x) nIflat.fits


#image -flat
imarith dz@B.list / nBflat.fits fdz@B.list
imarith dz@V.list / nVflat.fits fdz@V.list
imarith dz@R.list / nRflat.fits fdz@R.list
imarith dz@I.list / nIflat.fits fdz@I.list

