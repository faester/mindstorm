#!/bin/bash
source config.sh

leftpos=$(cat $left/position)
rightpos=$(cat $right/position)

r1=$(awk "BEGIN {print $standardLength - $leftpos/$degreesPerMilli}")
r2=$(awk "BEGIN {print $standardLength - $rightpos/$degreesPerMilli}")

echo $leftpos $r1 $rightpos $r2

x=$(awk "BEGIN {print ($r1 - $r2 + $width^2)/(2 * $width)}")
echo finding y
y=$(awk "BEGIN {print (sqrt($r1 * $r1 - $x * $x))}")

echo $x $y
