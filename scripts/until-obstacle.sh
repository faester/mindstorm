#!/bin/bash
source config 
./drive.sh 250 250
distance=$(cat $distanceSensor/value0)
while [ $distance -ge $minDistance ] 
do 
	echo "Clear ahead. ($distance)"
	sleep 0.1
	distance=$(cat $distanceSensor/value0)
done 
./stop.sh

