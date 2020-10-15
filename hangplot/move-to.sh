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
		cat $1/state
		sleep 1
	done
}

pos=($(./where-are-we-now.sh))
deltax=$(awk "BEGIN {print int(($targetx - ${pos[0]}) * $degreesPerMilli)}")
deltay=$(awk "BEGIN {print int(($targety - ${pos[1]}) * $degreesPerMilli)}")

speedX=100
speedY=$(awk "BEGIN {print int($speedX*($deltay/$deltax))}")
echo $deltax $deltay $speedX $speedY

./move-rel.sh l $deltax $speedX
./move-rel.sh r $deltay $speedY

wait_for_motor $left
wait_for_motor $right


