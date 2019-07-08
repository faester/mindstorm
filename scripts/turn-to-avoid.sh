#!/bin/bash
source config 
./drive.sh -350 350
distance=$(cat $distanceSensor/value0)
while [ $distance -le $minDistance ] 
do 
	echo "Obstacle ahead. ($distance)"
	sleep 0.3
	distance=$(cat $distanceSensor/value0)
done 
./stop.sh

