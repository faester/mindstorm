import math

class PointReader:
    def __init__(self):
        self.lines = []

    def distiance(self, a, b):
        (xa, ya) = a
        (xb, yb) = b
        return math.sqrt(((xa - xb) ** 2) + ((ya - yb) ** 2))

    def getLines(self):
        return self.lines

    def translate(self, translation):
        (tx, ty) = translation
        translated = []
        for points in self.lines:
            pointsNext = []
            for point in points:
                (x, y) = point
                pointsNext.append((x + tx, y + ty))
            translated.append(pointsNext)
        self.lines = translated
 
    def subdivide_lines(self, max_length):
        didSubdivide = 0
        subdivided = []
        for points in self.lines:
            lastPoint = None
            pointsNext = []
            for point in points:
                if (lastPoint != None):
                    d = self.distiance(lastPoint, point)
                    if (d > max_length):
                        didSubdivide = 1
                        (xlp, ylp) = lastPoint
                        (x, y) = point
                        auxPoint = ((x + xlp) / 2, (y + ylp) / 2)
                        pointsNext.append(auxPoint)
                pointsNext.append(point)
                lastPoint = point
            subdivided.append(pointsNext)
        self.lines = subdivided
        if didSubdivide: self.subdivide_lines(max_length)

    def read_points(self, filename):
        f=open(filename, 'r')
        result=[]
        lines=f.readlines()
        for line in lines:
            if line.startswith("#"): continue
            points=[]
            for element in line.split():
                if element != "":
                    coord=element.split(',')
                    points.append((int(coord[0]), int(coord[1])))
            result.append(points)
        self.lines = result

