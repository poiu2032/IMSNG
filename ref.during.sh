#!/bin/bash

code_DIR=/home/sylee/Desktop/LOAO/Guideline_code
ref_DIR=/home/sylee/Desktop/LOAO/red/astrometry/ref_fits

while read line
do
work_DIR=/home/sylee/Desktop/LOAO/red/astrometry/during
jpg_DIR=/home/sylee/Desktop/LOAO/red/astrometry/during_jpgcheck/


echo ${line}
	if [ -d $work_DIR/${line}/R ] ; then
		if [ -f $ref_DIR/${line}R*.fits ] ; then
			cd $work_DIR/${line}/R
			ls $work_DIR/${line}/R/acfdobj*${line}*.fits > countR.list
			countR=$(cat countR.list | wc -l)
			echo $countR
			if [ $countR -gt 0 ] ; then
				cp -rp $ref_DIR/${line}R*.fits $work_DIR/${line}/R/ref.fits
#				python $code_DIR/remap.py 
#				python $code_DIR/hotpantsrun.py 
#			ds9 -zscale hd*.fits ref.fits -single -zoom to fit -frame match wcs &	
#				cp -rp ~/sextractor/default* ./
				python $code_DIR/detect_loao.py

				cp -rp ./jpg/hd*R*jpg $jpg_DIR/${line}/R
				cp -rp ./jpg/ref.jpg $jpg_DIR/${line}/R/hdreacfdobj.${line}.${linea}.ref.jpg
				rm -rf reacfdobj*.fits obj.list default* 

			else
				echo "no hotpants"
			fi
		else
			echo "no R ref of ${line}"
		fi
	else
		echo "no R obj today"
	fi

	if [ -d $work_DIR/${line}/B ] ; then
		if [ -f $ref_DIR/${line}B*.fits ] ; then
			cd $work_DIR/${line}/B
			ls $work_DIR/${line}/B/acfdobj*${line}*.fits > countB.list
			countB=$(cat countB.list | wc -l)
			echo $countB
			if [ $countB -gt 0 ] ; then
				cp -rp $ref_DIR/${line}B*.fits $work_DIR/${line}/B/ref.fits
#				python $code_DIR/remap.py 
#				python $code_DIR/hotpantsrun.py 
	#		ds9 -zscale hd*.fits ref.fits -single -zoom to fit -frame match wcs &
#                                cp -rp ~/sextractor/default* ./
                                python $code_DIR/detect_loao.py

				cp -rp ./jpg/hd*B*.jpg $jpg_DIR/${line}/B
				cp -rp ./jpg/ref.jpg $jpg_DIR/${line}/B/hdreacfdobj.${line}.${linea}.ref.jpg

				rm -rf reacfdobj*.fits obj.list default* 
			else
				echo "no hotpants"
			fi
		else
			echo "no B ref of ${line}"
		fi

	else 
		echo "no B obj today"
	fi


rm -rf countR.list countB.list
done < /home/sylee/Desktop/LOAO/red/move.list

exit 0
