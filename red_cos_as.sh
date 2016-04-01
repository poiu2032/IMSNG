#!/bin/bash

code_DIR=/home/sylee/Desktop/LOAO/Guideline_code

while read line
do

cd /home/sylee/Desktop/LOAO/red/${line}


ls fdobj*.fits > cosmic.list
python $code_DIR/go_lacosmic_loao_cpu.py
python $code_DIR/astrometry.net.script_loao.py
python $code_DIR/fnamechange_loao.py

rm -rf astrometry_current_dir.sh bflat.list bobj.list cfdobj* cosmic.list default.sex dobj.*fits fdobj*.fits flat.list obj.list reduction_knu.cl rflat.list robj.list zero.list z?f.2x2*fits 

done < /home/sylee/Desktop/LOAO/red/date.list


sh < $code_DIR/move_acfdobj.sh

exit 0