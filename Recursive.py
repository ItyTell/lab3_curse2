from geom_classes import Point, Segment


def take_first(li):
    return li[0]


def recursion(points, segment):
    if len(points) <= 1:
        return points

    point_max = max(points, key=segment.height)
    left = []
    right = []
    segment_left = Segment(segment[0], point_max)
    segment_right = Segment(point_max, segment[1])
    for point in points:
        if segment_left.orientation(point) < 0:
            left.append(point)
        elif segment_right.orientation(point) < 0:
            right.append(point)

    result = recursion(left, segment_left)
    result.append(point_max)
    result += recursion(right, segment_right)
    return result


def recursive(edges):
    points = []
    for edge in edges:
        points.append(Point(edge))

    points.sort(key=take_first)

    left = points[0]
    right = points[-1]

    segment1 = Segment(left, right)
    segment2 = Segment(right, left)

    s1 = []
    s2 = []
    for point in points:
        if segment1.orientation(point) < 0:
            s1.append(point)
        elif segment1.orientation(point) > 0:
            s2.append(point)

    result = [left] + recursion(s1, segment1) + [right] + recursion(s2, segment2) + [left]
    return result



