from geom_classes import Point, Segment


def kirpatrik(edges):

    points = []
    for edge in edges:
        points.append(Point(edge))

