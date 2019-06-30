#!/bin/bash
source config 
./drive.sh 550 550
distance=$(cat $distanceSensor/value0)
while [ $distance -ge 25 ] 
do 
	echo "Clear ahead. ($distance)"
	sleep 0.1
	distance=$(cat $distanceSensor/value0)
done 
./stop.sh

