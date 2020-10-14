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

cat $output
