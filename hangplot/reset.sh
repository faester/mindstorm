#!/bin/bash
source config.sh

for m in $left $right $pen; do
	echo $m 
	echo reset >$m/command
done
