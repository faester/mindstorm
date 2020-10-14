#!/bin/bash
source config.sh
currentLeft=$1
currentRight=$2
if [[ "$currentLeft" == "" ]]; then 
	echo "Please specify current length of left wire."
	exit 1
fi
if [[ "$currentRight" == "" ]]; then 
	echo "Please specify current length of right wire."
	exit 2
fi

wait_for_motor() {
	while [ $(cat $1/state ) ]
	do
		cat $1/state
		sleep 1
	done
}

leftadjust=$(awk "BEGIN {print int((500 - $currentLeft)*$degreesPerMilli)}")
rightadjust=$(awk "BEGIN {print int((500 - $currentRight)*$degreesPerMilli)}")

leftspeed=100
rightspeed=$(awk "BEGIN {print int($leftspeed*($rightadjust/$leftadjust))}")

echo $leftadjust $leftspeed
echo $rightadjust $rightspeed

./move-rel.sh l $leftadjust $leftspeed
./move-rel.sh r $rightadjust $rightspeed

wait_for_motor $left
wait_for_motor $right



for m in $left $right $pen; do
	echo $m 
	echo reset >$m/command
done
