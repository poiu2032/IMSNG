#!/bin/sh


while read line
do
FILE_DIR=/home/sylee/Desktop/LOAO/red/astrometry/${line}
WORK_DIR=/home/sylee/Desktop/LOAO/red/astrometry/during

while read linea
do

#file=/data6/sy_LOAO/red/move.list



## Move ac*.fits and hd*.fits to folder 'all'
echo ${linea}
	if [ -d ${FILE_DIR}/${linea}/R ] ; then 
		mv $FILE_DIR/${linea}/R/cfdobj*R*fits $WORK_DIR/${linea}/R/
                mv $FILE_DIR/${linea}/R/acfdobj*R*fits $WORK_DIR/${linea}/R/
		rm -rf $FILE_DIR/${linea}/R
	else
	  echo "nothing"
	fi


        if [ -d ${FILE_DIR}/${linea}/B ] ; then
                mv $FILE_DIR/${linea}/B/cfdobj*B*fits $WORK_DIR/${linea}/B/
                mv $FILE_DIR/${linea}/B/acfdobj*B*fits $WORK_DIR/${linea}/B/
		rm -rf $FILE_DIR/${linea}/B
	else
          echo "nothing"
        fi


##remove empty folder
	ls $FILE_DIR/${linea}/R/*obj*.fits > countR.list
	countR=$(cat $FILE_DIR/${linea}/R/countR.list | wc -l)
	if [ $countR -gt 0 ] ; then echo "acfdobj?!"
	else	rm -rf $FILE_DIR/${linea}/R
	fi

	ls $FILE_DIR/${linea}/B/*obj*.fits > countB.list
	countB=$(cat $FILE_DIR/${linea}/B/countB.list | wc -l)
        if [ $countB -gt 0 ] ; then echo "acfdobj?!"
        else    rm -rf $FILE_DIR/${linea}/B
        fi

	if [ -d $FILE_DIR/${linea}/R ] ; then echo "R exist"
	elif [ -d $FILE_DIR/${linea}/B ] ; then echo "B exist"
	else rm -rf $FILE_DIR/${linea}
	fi

done < /home/sylee/Desktop/LOAO/red/move.list
done < /home/sylee/Desktop/LOAO/red/date.list
exit 0 

