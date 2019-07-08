#!/bin/bash
source config
speed=100

echo $speed >$motor0/speed_sp
echo -$speed >$motor1/speed_sp
echo run-forever>$motor0/command
echo run-forever>$motor1/command

watch -n 0.2 cat $distanceSensor/value0

./stop.sh
