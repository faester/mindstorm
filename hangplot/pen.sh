#!/bin/bash
if [[ $1 == "up" ]]; then 
	position=80
else 
	position=-80
fi

source config.sh
speed=200

echo $speed >$pen/speed_sp
echo $position >$pen/position_sp
echo run-to-rel-pos>$pen/command
