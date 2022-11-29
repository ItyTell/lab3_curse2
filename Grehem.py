from geom_classes import Point, Vector, Segment


def grehem(edges):

    points = []
    for edge in edges:
        points.append(Point(edge))

    point_0 = points[0]
    for point in points:
        if point_0[0] > point[0]:
            point_0 = point

    point_d = Point((point_0[0], point_0[1] + 10))
    segment_0 = Segment(point_0, point_d)
    vector_0 = Vector(point_0, point_d)

    def take_angle(point_1):
        if point_1 == point_0:
            return -100
        if segment_0.orientation(point_1) == 0:
            return 4

        vector_1 = Vector(point_0, point_1)
        cos_alfa = (vector_0 * vector_1) / (vector_1.norm() * vector_0.norm())

        return cos_alfa if segment_0.orientation(point_1) > 0 else 5 - cos_alfa

    points.sort(key=take_angle)

    result = [points[0], points[1]]
    for i in range(len(points) - 3):
        flag = True
        j = i + 2
        result.append(points[j])
        while flag:
            segment = Segment(result[-2], result[-1])
            if segment.orientation(points[j + 1]) < 0:
                flag = False
            else:
                result.pop(-1)

    result.append(points[-1])
    result.append(points[0])

    return result
