#!/bin/sh

while read lineg
do

FILE_DIR=/home/sylee/Desktop/LOAO/red/astrometry/all_server/all/${lineg}
echo ${lineg}


cd $FILE_DIR/R/
rm snap_* *.psf *.sml *.cat *.solved *.wcs *.axy *.corr *indx.xyls *.match *.rdls 

ls cfdobj*.fits > cfdobj.list
countcf=$(cat cfdobj.list | wc -l)
ls sacfdobj*.fits > sac.list
countsa=$(cat sac.list | wc -l)
ls acfdobj*.fits > ac.list
countac=$(cat ac.list | wc -l)
ls reacfdobj*.fits > re.list
countre=$(cat re.list | wc -l)
ls hdreac*.fits > hd.list
counthd=$(cat hd.list | wc -l)

echo $countsa $countcf $countac $countre $counthd

if [ $countcf -eq $countac] ; then
        rm cfdobj*.fits
fi

if [ $countre -eq $counthd ] ; then
        rm reacfdobj*.fits
fi


cd $FILD_DIR/B/
rm snap_* *.psf *.xml *.cat *.solved *.wcs *.axy *.corr .indx.xyls *.match *.rdls    

ls sacfdobj*.fits > sac.list
countsa=$(cat sac.list | wc -l)
ls cfdobj*.fits > cfdojb.list
countcf=$(cat cfdobj.list | wc -l)
ls acfdobj*.fits > ac.list
countac=$(cat ac.list | wc -l)
ls reacfdobj*.fits > re.list
countre=$(cat re.list | wc -l)
ls hdreac*.fits > hd.list
counthd=$(cat hd.list | wc -l)

echo $countsa $countac $countre $counthd

if [ $countcf -eq $countac ]; then
        rm cfdobj*.fits
fi

if [ $countri -eq $counthd ]; then
        rm reacfdobj*.fits
fi


done < ~/Desktop/LOAO/red/move.list



