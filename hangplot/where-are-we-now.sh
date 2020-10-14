#!/bin/bash
source config.sh

leftpos=$(cat $left/position)
rightpos=$(cat $right/position)

r1=$(awk "BEGIN {print $standardLength - $leftpos/$degreesPerMilli}")
r2=$(awk "BEGIN {print $standardLength - $rightpos/$degreesPerMilli}")
x=$(awk "BEGIN {print int(($r1 - $r2 + $width^2)/(2 * $width))}")
y=$(awk "BEGIN {print int(sqrt($r1 * $r1 - $x * $x))}")

echo $x $y
