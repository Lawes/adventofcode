
DIRECTIONS4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]

DIRECTIONS8 = DIRECTIONS4 + [(1, 1), (-1, -1), (1, -1), (-1, 1)]


def area_shoelace(points):
    X = [point[0] for point in points] + [points[0][0]]
    Y = [point[1] for point in points] + [points[0][1]]

    area = 0
    for i in range(len(points)):
        area += X[i] * Y[i + 1] - Y[i] * X[i + 1]

    return abs(area) / 2
