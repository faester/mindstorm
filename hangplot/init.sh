#!/bin/bash
output=config.sh
motordir=/sys/class/tacho-motor/
echo \# Created using init.sh it $(date)> $output
for m in $(ls $motordir); do
	fullpath=$motordir$m
	echo $m $fullpath
	address=$(cat $fullpath/address)
	if [[ "$address" == "ev3-ports:outA" ]]; then
		echo left=$fullpath >> $output
	fi
	if [[ "$address" == "ev3-ports:outB" ]]; then
		echo right=$fullpath >> $output
	fi
	if [[ "$address" == "ev3-ports:outD" ]]; then
		echo pen=$fullpath >> $output
	fi
done

degreesPerMilli=$(awk "BEGIN {print (1440/250)}")
echo degreesPerMilli=$degreesPerMilli >>$output
echo "What is the WIDTH between line anchors at top:"
read width 
echo width=$width  >> $output
echo standardLength=500 >> $output
cat $output

source config.sh

echo $left
echo $right
echo $pen
echo $width

output=config.py

echo "class Config:" >$output
echo "  def __init__(self):" >>$output
echo "    self.left = \"$left\"" >> $output
echo "    self.right = \"$right\"" >> $output
echo "    self.pen = \"$pen\"" >> $output
echo "    self.width = $width" >> $output
echo >> $output
echo "  def getLeftMotor(self): return self.left" >> $output
echo "  def getRightMotor(self): return self.right" >> $output
echo "  def getPenMotor(self): return self.pen" >> $output
echo "  def getAnchorDistance(self): return self.width" >> $output
