#!/bin/sh

while read line
do

FILE_DIR=/home/sylee/Desktop/LOAO/red/${line}
cp -rp /home/sylee/Desktop/LOAO/Guideline_code/reduction_knu.cl $FILE_DIR


done < /home/sylee/Desktop/LOAO/red/date.list

