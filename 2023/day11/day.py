import pycommon as M
import itertools


def load_input(filename):
    galaxies = []
    with open(filename, 'r') as f:
        for iy, line in enumerate(f):
            for ix, c in enumerate(line):
                if c == '#':
                    galaxies.append([ix, iy])
    return galaxies


def expand(points, factor=2):
    for icoord in [0, 1]:
        points.sort(key=lambda x: x[icoord])
        for ipt in range(1, len(points)):
            delta = points[ipt][icoord] - points[ipt-1][icoord]
            if delta > 1:
                for i in range(ipt):
                    points[i][icoord] -= (delta - 1) * (factor - 1)


def display(points):
    x, y = list(zip(*points))

    xrange = min(x), max(x)
    yrange = min(y), max(y)

    grid = []
    for _ in range(yrange[1] - yrange[0] + 1):
        grid.append(['.'] * (xrange[1] - xrange[0] + 1))

    for pt in points:
        grid[pt[1] - yrange[0]][pt[0] - xrange[0]] = '#'

    for row in grid:
        print(''.join(row))


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    display(data)
    expand(data)
    display(data)


@M.timeperf
def part1():
    points = load_input('input')
    expand(points)

    s = 0
    for pt1, pt2 in itertools.combinations(points, 2):
        s += abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
    print('part1', s)


@M.timeperf
def part2():
    points = load_input('input')
    expand(points, factor=1000000)

    s = 0
    for pt1, pt2 in itertools.combinations(points, 2):
        s += abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
    print('part2', s)


if __name__ == '__main__':
    test()
    part1()
    part2()
