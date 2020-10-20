import sys
import time
import math

from config import Config
from plotter import Plotter

config = Config()
print(config.getLeftMotor())
print(config.getRightMotor())
print(config.getPenMotor())
print(config.getAnchorDistance())
plotter = Plotter(config)

if len(sys.argv) != 4:
    print("Expecting three parameters: translate x, translate y, pointsfile")
    exit 

translate=(int(sys.argv[1]), int(sys.argv[2]))

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


plotter.pen_mode(0)
plotter.move_to(translate)
points = read_points(sys.argv[3])
print(points)
exit(1)

for line in points:
    first=1
    for point in line:
        translated=(point[0] + translate[0], point[1] + translate[1])
        move_to(translated)
        if first:
            first=0
            pen_mode(1)
                
    if not first: pen_mode(0)
