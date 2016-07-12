#!/bin/sh


while read line
do
FILE_DIR=/home/sylee/Desktop/LOAO/red/astrometry/during/${line}
WORK_DIR=/home/sylee/Desktop/LOAO/red/astrometry/all/${line}


#file=/data6/sy_LOAO/red/move.list



## Move ac*.fits and hd*.fits to folder 'all'
echo ${line}
	cd $FILE_DIR/R/
	ls hd*R*.fits > counthdR.list

        hdR=$(cat counthdR.list | wc -l)
        if [ $hdR -gt 0 ] ; then		
		mv h?reacfdobj*R* $WORK_DIR/R/
		mv ./jpg/*${line}*.jpg ${WORK_DIR%${line}}/jpg/${line}/R/
		while read linea
		do
			mv ${linea#hdre} $WORK_DIR/R/
		done < counthdR.list

	else
	  echo "nothing"
	fi



        cd $FILE_DIR/B/
        ls hd*B*.fits > counthdB.list
        
        hdB=$(cat counthdB.list | wc -l)
        if [ $hdB -gt 0 ] ; then
                mv h?reacfdobj*B* $WORK_DIR/B/
		mv ./jpg/*${line}*.jpg ${WORK_DIR%${line}}/jpg/${line}/B/
                while read linea
                do
                        mv ${linea#hdre} $WORK_DIR/B/
                done < counthdB.list
	else
          echo "nothing"
        fi


##remove empty folder
#	ls $FILE_DIR/${linea}/R/*cfdobj*.fits > countR.list
#	countR=$(cat $FILE_DIR/${linea}/R/countR.list | wc -l)
#	if [ $countR -gt 0 ] ; then echo "acfdobj?!"
#	else	rm -rf $FILE_DIR/${linea}/R
#	fi

#	ls $FILE_DIR/${linea}/B/*cfdobj*.fits > countB.list
#	countB=$(cat $FILE_DIR/${linea}/B/countB.list | wc -l)
#       if [ $countB -gt 0 ] ; then echo "acfdobj?!"
#      else    rm -rf $FILE_DIR/${linea}/B
#       fi

#	if [ -d $FILE_DIR/${linea}/R ] ; then echo "R exist"
#	elif [ -d $FILE_DIR/${linea}/B ] ; then echo "B exist"
#	else rm -rf $FILE_DIR/${linea}
#	fi

done < /home/sylee/Desktop/LOAO/red/move.list
exit 0 

