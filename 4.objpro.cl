
!gethead *.fits FILTER OBJECT IMAGETYP EXPTIME

ls *.fits > obj.list
#hselect @obj.list $I "filter='U(Y)'" > yobj.list ;type yobj.list
#hselect @obj.list $I "filter='U'" > uobj.list ;type uobj.list
hselect @obj.list $I "filter='R'" > robj.list ; type robj.list
hselect @obj.list $I "filter='B'" > bobj.list ; type bobj.list
#hselect @obj.list $I "filter='V'" > vobj.list ; type vobj.list
#hselect @obj.list $I "filter='R(Ha)'" > raobj.list ; type raobj.list
#hselect @obj.list $I "filter='I'" > iobj.list ; type iobj.list

imarith @obj.list - ../bias/zero.fits z@obj.list

imarith z@bobj.list / ../flat/nbflat.fits fz@bobj.list
#imarith z@raobj.list / ../flat/nraflat.fits fz@raobj.list
imarith z@robj.list / ../flat/nrflat.fits fz@robj.list
#imarith z@raobj.list / ../flat/nrflat.fits fz@raobj.list
#imarith z@vobj.list / ../flat/nvflat.fits fz@vobj.list
#imarith z@iobj.list / ../flat/niflat.fits fz@iobj.list

!ds9 fz*.fits &
ls fz*.fits > all.list

ls
#!python /home/lim9/Desktop/IMSNG/9codes/automatic_1d_maidanak/5.bgscale_1d_maidanak.py
