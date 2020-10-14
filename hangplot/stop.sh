#!/bin/bash
source config.sh
for m in $left $right $pen; do
	echo stopping $m
	echo stop >> $m/command
done
