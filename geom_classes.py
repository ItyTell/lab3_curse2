import numpy as np


class Point:

    def __init__(self, cords):
        self.cords = np.array(cords)

    def __getitem__(self, val):
        return self.cords[val]


class Segment:

    def __init__(self, point1, point2):
        self.points = [point1, point2]

    def __getitem__(self, val):
        return self.points[val]

    def orientation(self, point):
        return (self[1][0] - self[0][0]) * (point[1] - self[1][1]) - \
               (self[1][1] - self[0][1]) * (point[0] - self[1][0])

    def height(self, point):
        d1 = self[0].cords - point.cords
        d2 = self[1].cords - point.cords
        return abs(d1[0] * d2[1] - d2[0] * d1[1])


class Vector:

    def __init__(self, point1, point2):
        self.d = point2.cords - point1.cords

    def norm(self):
        return (self.d[0] ** 2 + self.d[1] ** 2) ** (1/2)

    def __mul__(self, other):
        return self.d[0] * other.d[0] + self.d[1] * other.d[1]
