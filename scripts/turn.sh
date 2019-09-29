#!/bin/bash
source config
echo $1
amount0=$(awk "BEGIN {print ($1 / 360) * 1368}")
amount1=$(awk "BEGIN {print -1 * $amount0}")
echo "amount $d360"

#echo $lSpeed>$motor0/speed_sp
#echo $rSpeed>$motor1/speed_sp
rSpeed=$2
echo $amount0 >/sys/class/tacho-motor/motor1/position_sp  
echo $amount1 >/sys/class/tacho-motor/motor0/position_sp

echo run-to-rel-pos>$motor0/command
echo run-to-rel-pos>$motor1/command
