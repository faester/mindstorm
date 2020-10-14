#!/bin/bash
source config.sh

for m in $left $right $pen; do
	echo "$m state=$(cat $m/state) speed=$(cat $m/speed) pos=$(cat $m/position)"
done
