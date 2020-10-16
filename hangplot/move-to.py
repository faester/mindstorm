import sys
import time
import math

target=(int(sys.argv[1]), int(sys.argv[2]))

left='/sys/class/tacho-motor/motor0'
right='/sys/class/tacho-motor/motor1'
pen='/sys/class/tacho-motor/motor2'
degreesPerMilli=5.76
width=430
standardLength=500

def read_file(filename):
    f=open(filename, 'r')
    content=f.read()
    f.close()
    return content.strip()

def degrees(motor):
    return int(read_file(motor + '/position'))

def to_wire_length(position):
    left=position[0] ** 2
    height=position[1] ** 2
    opposite=(width-position[0]) ** 2
    return (math.sqrt(left + height), math.sqrt(opposite + height))

def write_file(filename, content):
    f=open(filename, 'w')
    f.write(content)
    f.close()

def start_move(motor, target_position, speed):
    write_file(motor + '/position_sp', str(int(target_position)))
    write_file(motor + '/speed_sp', str(int(speed)))
    write_file(motor + '/command', 'run-to-rel-pos')

def wait_for(motor):
    while read_file(motor + '/state') == 'running':
        print ('Waiting for ' + motor)
        time.sleep(1)

current_wires=(standardLength + degrees(left)/degreesPerMilli,standardLength + degrees(right)/degreesPerMilli)

print (left, right, target)
print (current_wires)
target_wires=to_wire_length(target)
print (target_wires)
adjust=(degreesPerMilli * (target_wires[0]-current_wires[0]),degreesPerMilli * (target_wires[1]-current_wires[1]))
print (adjust)
speed=(100, 100 * adjust[1] / adjust[0])
start_move(left, adjust[0], speed[0])
start_move(right, adjust[1], speed[1])
wait_for(left)
wait_for(right)
