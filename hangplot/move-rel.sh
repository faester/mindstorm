#!/bin/bash
moveleft=0
moveright=0
if  [[ "$1" =~ l ]]; then 
	moveleft=1
fi
if [[ "$1" =~ r ]]; then
	moveright=1
fi
relpos=$2
speed=100

source config.sh

echo $moveleft
echo $moveright

move_motor() {
	motor=$1
	speed=$2
	position=$3
	echo "Doing! $motor $speed $position"
	echo $position > $motor/position_sp
	echo $speed > $motor/speed_sp
	echo run-to-rel-pos > $motor/command
}

if [ $moveleft ]; then 
	move_motor $left $speed $relpos
fi

if [ $moveright ]; then
	move_motor $right $speed $relpos
fi

#echo $speed >$left/speed_sp
#echo -$speed >$right/speed_sp
#echo run-forever>$left/command
#echo run-forever>$right/command
