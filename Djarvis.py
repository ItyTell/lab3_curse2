from geom_classes import Point, Segment


def take_first(li):
    return li[0]


def djarvis(edges):

    points = []
    for edge in edges:
        points.append(Point(edge))

    points.sort(key=take_first)

    left = points[0]

    result = [left]
    for point in points[1::]:
        segment = Segment(result[-1], point)
        flag = True
        for point2 in points:
            if segment.orientation(point2) > 0:
                flag = False
                break
        if flag:
            result.append(point)

    for point in points[-2::-1]:
        segment = Segment(result[-1], point)
        flag = True
        for point2 in points:
            if segment.orientation(point2) > 0:
                flag = False
                break
        if flag:
            result.append(point)

    return result
