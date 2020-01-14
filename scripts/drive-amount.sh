#!/bin/bash
source config
echo $1
amount0=$(awk 'BEGIN {print (($1 / 360) * 1000)}')
echo "amount $amount0"

rSpeed=$2
echo $amount0 >/sys/class/tacho-motor/motor1/position_sp  
echo $amount0 >/sys/class/tacho-motor/motor0/position_sp

echo run-to-rel-pos>$motor0/command
echo run-to-rel-pos>$motor1/command
