#!/bin/bash
source config.sh
targetx=$1
targety=$2
if [[ "$targetx" == "" ]]; then
	echo "Specify target x"
	exit 1
fi
if [[ "$targety" == "" ]]; then
	echo "Specify target y"
	exit 2
fi

wait_for_motor() {
	while [ $(cat $1/state ) ]
	do
		echo Waiting for $1
		cat $1/state
		sleep 1
	done
}

current_length() {
	position=$(cat $1/position)
	length=$(awk "BEGIN {print int($standardLength-$position*$degreesPerMilli)}")
	echo $length
}

pos=($(./where-are-we-now.sh))

let oppositeX=$width-$targety
desiredLengthLeft=$(awk "BEGIN {print int(sqrt($targetx*$targetx + $targety*$targety )) } ")
desiredLengthRight=$(awk "BEGIN {print int(sqrt($oppositeX*$oppositeX + $targety*$targety )) } ")

echo Desired length $desiredLengthLeft $desiredLengthRight

let currentLeft=$(current_length $left)
let currentRight=$(current_length $right)
echo Current $currentLeft $currentRight

let deltaleft=$desiredLengthLeft-$currentLeft
let deltaright=$desiredLengthRight-$currentRight

degreesleft=$(awk "BEGIN {print int($deltaleft * $degreesPerMilli)}")
degreesright=$(awk "BEGIN {print int($deltaright * $degreesPerMilli)}")

speedleft=100
speedright=$(awk "BEGIN {print int($speedleft * ($deltaright / $deltaleft))}")

echo Deltas $deltaleft $deltaright
echo Adjust $degreesleft $degreesright $speedleft $speedright

#./move-rel.sh l $degreesleft $speedleft
#./move-rel.sh r $degreesright $speedright

wait_for_motor $left
wait_for_motor $right


