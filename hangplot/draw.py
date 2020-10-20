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
pointReader.subdivide_lines()
points = pointReader.getLines()
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
