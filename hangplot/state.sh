#!/bin/bash
source config.sh

for m in $left $right $pen; do
	echo $m ::::::
	cat $m/state
	cat $m/speed
	cat $m/position
done
