#!/bin/bash

code_DIR=/home/sylee/Desktop/LOAO/Guideline_code

while read line
do

cd /home/sylee/Desktop/LOAO/red/${line}


ls fdobj*.fits > cosmic.list
rename 's/M51a/MESSIER051a/;' *M51a*
rename 's/M63/MESSIER063/;' *M63*
rename 's/M64/MESSIER064/;' *M64*
rename 's/M99/MESSIER099/;' *M99* 
rename 's/M101/MESSIER101/;' *M101*
#python $code_DIR/fnamechange_loao.py
python $code_DIR/go_lacosmic_loao_cpu.py
python $code_DIR/astrometry.net.script_loao.py

rm -rf astrometry_current_dir.sh bflat.list bobj.list cosmic.list default.sex dobj.*fits fdobj*.fits flat.list obj.list reduction_knu.cl rflat.list robj.list zero.list z?f.2x2*fits *.wcs *.xyls *.axy *.corr *.match *.rdls

done < /home/sylee/Desktop/LOAO/red/date.list


sh < $code_DIR/move_acfdobj.sh

while read line
do

ls /home/sy_LOAO/Desktop/LOAO/red/${line}/ac*.fits > acfdobj.list
cat /home/sy_LOAO/Desktop/LOAO/red/${line}/countR.list | wc -l

done < /home/sylee/Desktop/LOAO/red/date.list

exit 0
