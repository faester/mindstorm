import sys
import time
import math

if len(sys.argv) != 4:
    print("Expecting three parameters: translate x, translate y, pointsfile")
    exit 

translate=(int(sys.argv[1]), int(sys.argv[2]))

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

def get_speed(desired_speed, speed):
    max_speed = max(abs(speed[0]), abs(speed[1]))
    scale = desired_speed / max_speed
    return (abs(speed[0] * scale), abs(speed[1] * scale))

def move_to(target):
    current_wires=(standardLength + degrees(left)/degreesPerMilli,standardLength + degrees(right)/degreesPerMilli)
    print (left, right, target)
    print (current_wires)
    target_wires=to_wire_length(target)
    print (target_wires)
    adjust=(degreesPerMilli * (target_wires[0]-current_wires[0]),degreesPerMilli * (target_wires[1]-current_wires[1]))
    print (adjust)
    speed=get_speed(100, adjust)
    print (speed)
    start_move(left, adjust[0], speed[0])
    start_move(right, adjust[1], speed[1])
    wait_for(left)
    wait_for(right)

def pen_mode(down):
    write_file(pen + '/speed_sp', '100')
    if down:
        write_file(pen + '/position_sp', '30')
    else:
        write_file(pen + '/position_sp', '-30')
    write_file(pen + '/command', 'run-to-rel-pos')
    wait_for(pen)

def read_points(filename):
    f=open(filename, 'r')
    result=[]
    lines=f.readlines()
    for line in lines:
        points=[]
        for element in line.split():
            if element != "":
                coord=element.split(',')
                points.append((int(coord[0]), int(coord[1])))
        result.append(points)
    return result


move_to(translate)
points = read_points(sys.argv[3])
print(points)

for line in points:
    first=1
    pen_mode(0)
    for point in line:
        translated=(point[0] + translate[0], point[1] + translate[1])
        if first:
            first=0
            pen_mode(1)
        move_to(translated)

