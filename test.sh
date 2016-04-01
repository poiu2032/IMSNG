#!/bin/sh

while read lineA
do
echo $lineA

while read lineB
do
echo $lineB
done < fb.list

done < fa.list

exit 0
