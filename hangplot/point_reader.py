import math

class PointReader:
    def __init__(self):
        self.lines = []
        self.max_length = 20

    def distiance(self, a, b):
        (xa, ya) = a
        (xb, yb) = b
        return math.sqrt(((xa - xb) ** 2) + ((ya - yb) ** 2))

    def getLines(self):
        return self.lines

    def subdivide_lines(self):
        didSubdivide = 0
        subdivided = []
        for points in self.lines:
            lastPoint = None
            pointsNext = []
            for point in points:
                if (lastPoint != None):
                    d = self.distiance(lastPoint, point)
                    if (d > self.max_length):
                        print("subdividing", d)
                        didSubdivide = 1
                        (xlp, ylp) = lastPoint
                        (x, y) = point
                        auxPoint = ((x + xlp) / 2, (y + ylp) / 2)
                        pointsNext.append(auxPoint)
                pointsNext.append(point)
                lastPoint = point
            subdivided.append(pointsNext)
        self.lines = subdivided
        if didSubdivide: self.subdivide_lines()

    def read_points(self, filename):
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
        self.lines = result

