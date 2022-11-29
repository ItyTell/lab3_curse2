import numpy as np


class Edge:

    edges = []

    def __init__(self, cords):

        self.cords = np.array(cords)
        Edge.edges.append(self)

    def __getitem__(self, val):
        return self.cords[val]

    def __len__(self):
        return 2

    def distance(self, cords):
        d = self.cords - cords
        return ((d[0]) ** 2 + (d[1]) ** 2) ** 0.5


class Segment:

    segments = []

    def __init__(self, cords):
        self.x = np.array([cords[0], cords[1]])
        self.y = np.array([cords[2], cords[3]])
        Segment.segments.append(self)

