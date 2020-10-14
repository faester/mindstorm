#!/bin/bash
moveleft=false
moveright=false
if  [[ "$1" =~ l ]]; then 
	echo moveleft
	moveleft=true
fi
if [[ "$1" =~ r ]]; then
	echo moveright
	moveright=true
fi
relpos=$2
speed=$3
if [[ "$speed" == "" ]]; then 
	speed=100
fi

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

if [ "$moveleft" = true ]; then 
	move_motor $left $speed $relpos
fi

if [ "$moveright" = true ]; then
	move_motor $right $speed $relpos
fi

#echo $speed >$left/speed_sp
#echo -$speed >$right/speed_sp
#echo run-forever>$left/command
#echo run-forever>$right/command
