#!/bin/bash
source config
lSpeed=$1
rSpeed=$2

echo $lSpeed>$motor0/speed_sp
echo $rSpeed>$motor1/speed_sp

echo run-forever>$motor0/command
echo run-forever>$motor1/command
