#!/bin/bash
source config.sh
speed=50

echo $speed >$left/speed_sp
echo -$speed >$right/speed_sp
echo run-forever>$left/command
echo run-forever>$right/command
