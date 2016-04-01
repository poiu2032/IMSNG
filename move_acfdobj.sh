!/bin/bash
while read lineb
do


FILE_DIR=/home/sylee/Desktop/LOAO/red/${lineb}
WORK_DIR=/home/sylee/Desktop/LOAO/red/astrometry/${lineb}
mkdir /home/sylee/Desktop/LOAO/red/astrometry/${lineb}


while read linea
do 

	cd $FILE_DIR
	ls acfdobj*${linea}*R*.fits > countR.list
	countR=$(cat countR.list | wc -l)
	echo $countR
	if [ $countR -gt 0  ] ; then 
		mkdir $WORK_DIR/${linea}
		mkdir $WORK_DIR/${linea}/R
		mv $FILE_DIR/cfdobj*${linea}*R*.fits $WORK_DIR/${linea}/R/
		mv $FILE_DIR/acfdobj*${linea}*R*.fits $WORK_DIR/${linea}/R/
		rm countR.list
	else
	  echo "false"
	fi


	cd $FILE_DIR
        ls acfdobj*${linea}*B*.fits > countB.list
        countB=$(cat countB.list | wc -l)
	echo $countB
        if [ $countB -gt 0 ] ; then

                mkdir $WORK_DIR/${linea}
		mkdir $WORK_DIR/${linea}/B

                mv $FILE_DIR/cfdobj*${linea}*B*.fits $WORK_DIR/${linea}/B/ 
                mv $FILE_DIR/acfdobj*${linea}*B*.fits $WORK_DIR/${linea}/B/ 
		rm countB.list
        else
          echo "false"
        fi



done < /home/sylee/Desktop/LOAO/red/move.list

done < /home/sylee/Desktop/LOAO/red/date.list

exit 0 

