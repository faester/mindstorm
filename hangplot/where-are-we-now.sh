#!/bin/bash
source config.sh

leftpos=$(cat $left/position)
rightpos=$(cat $right/position)

r1=$(awk "BEGIN {print $leftpos/$degreesPerMilli}")
r2=$(awk "BEGIN {print $rightpos/$degreesPerMilli}")

echo $leftpos $r1 $rightpos $r2
