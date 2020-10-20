#!/bin/bash
source config.sh
speed=$1

if [[ $speed == "" ]]; then
	speed=50
fi

echo -$speed >$left/speed_sp
echo -$speed >$right/speed_sp
echo run-forever>$left/command
echo run-forever>$right/command
