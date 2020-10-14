#!/bin/bash
output=config.sh
motordir=/sys/class/tacho-motor/
echo \# Created using init.sh it $(date)> $output
for m in $(ls $motordir); do
	fullpath=$motordir$m
	echo $m $fullpath
	address=$(cat $fullpath/address)
	if [[ "$address" == "ev3-ports:outA" ]]; then
		echo left=$fullpath >> $output
	fi
	if [[ "$address" == "ev3-ports:outB" ]]; then
		echo right=$fullpath >> $output
	fi
	if [[ "$address" == "ev3-ports:outD" ]]; then
		echo pen=$fullpath >> $output
	fi
done

degreesPerMilli=$(awk "BEGIN {print (1440/250)}")
echo degreesPerMilli=$degreesPerMilli >>$output
echo "What is the length of LEFT line in mm:"
read leftlength
echo "What is the length of RIGHT line in mm:"
read rightlength
echo "What is the WIDTH between line anchors at top:"
read width 
echo leftlength=$leftlength >> $output
echo rightlength=$rightlength >> $output
echo width=$width  >> $output

cat $output
