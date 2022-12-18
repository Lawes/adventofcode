import numpy as np


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            multiline = [[int(e) for e in item.split(',')] for item in line.replace('->', '').split()]
            res.append(multiline)
    return res


def order(x1, x2):
    return (x1, x2) if x1 < x2 else (x2, x1)


def moves(xs, grid):
    pt = (xs, 0)
    while True:
        newd = pt[1] + 1
        if grid[newd, pt[0]] == 0:
            pt = (pt[0], newd)
        elif grid[newd, pt[0]-1] == 0:
            pt = (pt[0]-1, newd)
        elif grid[newd, pt[0]+1] == 0:
            pt = (pt[0]+1, newd)
        else:
            return pt

        if pt[1] == grid.shape[0]-1:
            return None


def change_coords(mlines, x0, d0):
    def conv(x, d):
        return (x - x0, d - d0)
    return [[conv(*pt) for pt in line] for line in mlines]


def place_rocks(mlines, grid):
    for line in mlines:
        for pt1, pt2 in zip(line[:-1], line[1:]):
            if pt1[0] == pt2[0]:
                d1, d2 = order(pt1[1], pt2[1])
                grid[d1:d2+1, pt1[0]] = 2
            elif pt1[1] == pt2[1]:
                x1, x2 = order(pt1[0], pt2[0])
                grid[pt1[1], x1:x2+1] = 2


def part1():
    mlines = load_input('input')

    xx = []
    dd = []
    for line in mlines:
        x, d = zip(*line)
        xx.extend(x)
        dd.extend(d)

    x0 = np.min(xx)-1
    d0 = 0

    nx = np.max(xx) - x0 + 2
    nd = np.max(dd) - d0 + 2

    grid = np.zeros((nd, nx))

    xs = 500 - x0

    mlines = change_coords(mlines, x0, d0)
    place_rocks(mlines, grid)
    print(grid)

    count = 0
    while True:
        pt = moves(xs, grid)
        if pt is None:
            break
        count += 1
        grid[pt[1], pt[0]] = 1
    print('part1', count)


def part2():
    mlines = load_input('input')

    xx = []
    dd = []
    for line in mlines:
        x, d = zip(*line)
        xx.extend(x)
        dd.extend(d)

    d0 = 0
    nd = np.max(dd) - d0 + 3
    dx = max(500 - np.min(xx), np.max(xx) - 500, nd)
    x0 = 500 - dx
    nx = 2 * dx + 1

    grid = np.zeros((nd, nx))

    print(grid)

    xs = 500 - x0

    mlines.append([(x0, d0 + nd - 1), (x0 + nx - 1, d0 + nd - 1)])
    mlines = change_coords(mlines, x0, d0)
    place_rocks(mlines, grid)

    count = 0
    while True:
        pt = moves(xs, grid)
        if pt is None:
            break
        if pt[1] == 0:
            break
        count += 1
        grid[pt[1], pt[0]] = 1
    print('part2', count+1)


if __name__ == '__main__':
    part1()
    part2()
