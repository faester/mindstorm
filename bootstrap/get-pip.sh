#!/bin/bash
# We cannot apt install pip on ev3dev
# this is just a small utility to over-
# come this obstacle.
#

getpip=$(pwd)/get-pip.py
echo "Getting $getpip if needed..."
if [ -f "$getpip" ]; then 
	echo "File $getpip already existed.		"
else 
	echo "Starting download."
	wget https://bootstrap.pypa.io/get-pip.py 
fi
echo "Starting get-pip.py"
python3 $getpip --user
