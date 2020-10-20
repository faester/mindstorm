import sys
import time
import math

from config import Config
from plotter import Plotter
from point_reader import PointReader

config = Config()
plotter = Plotter(config)
pointReader = PointReader()

if len(sys.argv) != 4:
    print("Expecting three parameters: translate x, translate y, pointsfile")
    exit 

translate=(int(sys.argv[1]), int(sys.argv[2]))

plotter.pen_mode(0)
plotter.move_to(translate)
pointReader.read_points(sys.argv[3])
points = pointReader.getLines()
print(points)
pointReader.subdivide_lines(10)
points = pointReader.getLines()
print(points)
pointReader.translate(translate)
points = pointReader.getLines()
print(points)

for line in points:
    first=1
    for point in line:
        print (point, end = ' ')
        plotter.move_to(point)
        if first:
            first=0
            plotter.pen_mode(1)
    print()
                
    if not first: plotter.pen_mode(0)
