import re

coord_pattern = re.compile(r'x=(-?\d+), y=(-?\d+)')


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            tokens = coord_pattern.findall(line)
            if len(tokens) != 2:
                continue
            sensor = (int(tokens[0][0]), int(tokens[0][1]))
            beacon = (int(tokens[1][0]), int(tokens[1][1]))
            dist = manhattan(sensor, beacon)
            res.append({'sensor': sensor, 'beacon': beacon, 'd': dist})
    return res


def yintersect(pt, dist, y0):
    x, y = pt
    dy = abs(y - y0)
    if dy > dist:
        return None

    x1 = x - (dist - dy)
    x2 = x + (dist - dy)

    return x1, x2


def isjoin(i1, i2):
    return i1[1] >= i2[0]


def yproject(data, y0):
    xintervals = []
    for item in data:
        xr = yintersect(item['sensor'], item['d'], y0)
        if xr is not None:
            xintervals.append(xr)
    xintervals.sort()

    final = []
    current = xintervals[0]
    for test in xintervals[1:]:
        if isjoin(current, test):
            current = (current[0], max(test[1], current[1]))
        else:
            final.append(current)
            current = test
    final.append(current)
    return final


def part1():
    # data = load_input('input_test')
    # y0 = 11
    data = load_input('input')
    y0 = 2000000
    print(data)

    intervals = yproject(data, y0)

    print(intervals)

    count = 0
    for t in intervals:
        count += t[1] - t[0]
    print('part1', count)


def part2():
    data = load_input('input')

    for y in range(4000000):
        intervals = yproject(data, y)
        if len(intervals) > 1:
            print(intervals[0][1]+1, y)
            break
    print('part2', (intervals[0][1]+1) * 4000000 + y)


if __name__ == '__main__':
    part2()






