#!/bin/sh

while read line
do

FILE_DIR=/home/sylee/Desktop/LOAO/red/astrometry/${line}
WORK_DIR=/home/sylee/Desktop/LOAO/red/astrometry/all
while read linea
do



#file=/data6/sy_LOAO/red/move.list



## Move ac*.fits and hd*.fits to folder 'all'
echo ${linea}
	cd $FILE_DIR/${linea}/R/
	ls hd*R*.fits > counthdR.list
	hdR=$(cat counthdR.list | wc -l)
	if [ $hdR -gt 0 ] ; then 
		mv $FILE_DIR/${linea}/R/h?reacfdobj*R* $WORK_DIR/${linea}/R/
                mv $FILE_DIR/${linea}/R/acfdobj*R* $WORK_DIR/${linea}/R/
		mv /home/sylee/Desktop/LOAO/red/astrometry/jpgcheck/${line}/*${linea}*R*.jpg $WORK_DIR/jpg/${linea}/R/
		rm -rf $FILE_DIR/${linea}/R 
	else
	  echo "nothing"
	fi


	cd $FILE_DIR/${linea}/B/
	ls hd*B*.fits > counthdB.list
	hdB=$(cat counthdB.list | wc -l)
        if [ $hdB -gt 0 ] ; then
                mv $FILE_DIR/${linea}/B/h?reacfdobj*B*fits $WORK_DIR/${linea}/B/
                mv $FILE_DIR/${linea}/B/acfdobj*B*fits $WORK_DIR/${linea}/B/
                mv /home/sylee/Desktop/LOAO/red/astrometry/jpgcheck/${line}/*${linea}*B*.jpg $WORK_DIR/jpg/${linea}/B/
		rm -rf $FILE_DIR/${linea}/B 
	else
          echo "nothing"
        fi


##remove empty folder
	if [ -d $FILE_DIR/${linea}/R -a -d $FILE_DIR/${linea}/B ] ; then echo "R,B exist!"
	elif [ -d $FILE_DIR/${linea}/R ] ; then echo "R exist!"
	elif [ -d $FILE_DIR/${linea}/B ] ; then echo "B exist!"
	else	rm -rf $FILE_DIR/${linea}
	fi

done < /home/sylee/Desktop/LOAO/red/move.list
done < /home/sylee/Desktop/LOAO/red/date.list
exit 0 

