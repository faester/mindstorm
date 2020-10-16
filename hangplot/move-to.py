import sys
import math

target=(int(sys.argv[1]), int(sys.argv[2]))

left='/sys/class/tacho-motor/motor0'
right='/sys/class/tacho-motor/motor1'
pen='/sys/class/tacho-motor/motor2'
degreesPerMilli=5.76
width=430
standardLength=500

def degrees(motor):
    file=open(motor + '/position', 'r')
    return int(file.read())

def to_wire_length(position):
    left=position[0] ** 2
    height=position[1] ** 2
    opposite=(width-position[0]) ** 2
    return (math.sqrt(left + height), math.sqrt(opposite + height))

currentWires=(standardLength + degrees(left)/degreesPerMilli,standardLength + degrees(right)/degreesPerMilli)



print (left, right, target)
print (currentWires)
print (to_wire_length(target))
