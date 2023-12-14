import pycommon as M
from collections import defaultdict


def load_input(filename):
    rocks = []
    sands = []

    with open(filename, 'r') as f:
        content = f.read().splitlines()
        size = len(content[0])
        for iy, line in enumerate(content):
            for ix, c in enumerate(line):
                if c == '#':
                    rocks.append((ix, iy))
                elif c == 'O':
                    sands.append((ix, iy))

    return frozenset(rocks), frozenset(sands), size


def tilt(rocks, sands, size, axis=1, dir=-1):
    static_sands = set()
    percol = defaultdict(list)

    oaxis = (axis + 1) % 2

    for s in sands:
        percol[s[oaxis]].append(s[axis])

    for fix, lvalues in percol.items():
        for v in sorted(lvalues, reverse=(dir>0)):
            while True:
                v += dir
                pt = [0, 0]
                pt[oaxis] = fix
                pt[axis] = v
                pt = tuple(pt)

                if pt in rocks or pt in static_sands or v < 0 or v >= size:
                    pt = list(pt)
                    pt[axis] -= dir

                    static_sands.add(tuple(pt))
                    break
    return frozenset(static_sands)


def ranges_from_pt(*points):
    x, y = list(zip(*points))
    xrange = min(x), max(x)
    yrange = min(y), max(y)
    return xrange, yrange


def display(p1, p2):
    xrange, yrange = ranges_from_pt(*p1, *p2)

    grid = []
    for _ in range(yrange[1] - yrange[0] + 1):
        grid.append(['.'] * (xrange[1] - xrange[0] + 1))

    for pt in p1:
        grid[pt[1] - yrange[0]][pt[0] - xrange[0]] = '#'

    for pt in p2:
        grid[pt[1] - yrange[0]][pt[0] - xrange[0]] = '0'

    return '\n'.join(''.join(row) for row in grid)


def load(rocks, sands):
    M.debug(display(rocks, sands))
    xrange, yrange = ranges_from_pt(*rocks)
    dy = yrange[1] - yrange[0]
    s = 0
    for pt in sands:
        s += dy - pt[1] + 1
    return s


@M.timeperf
def test():
    M.log()
    rocks, sands, size = load_input('input_test')
    sands = tilt(rocks, sands, size)
    s = load(rocks, sands)
    print(s)


@M.timeperf
def part1():
    rocks, sands, size = load_input('input')
    sands = tilt(rocks, sands, size)
    print('part1', load(rocks, sands))


@M.timeperf
def part2():
    # M.nolog()
    rocks, sands, size = load_input('input')

    tiltcycle = [
        {'axis': 1, 'dir': -1},
        {'axis': 0, 'dir': -1},
        {'axis': 1, 'dir': 1},
        {'axis': 0, 'dir': 1},
    ]

    cache = {}
    cycle = 0
    while cycle < 1000000000:
        for tiltargs in tiltcycle:
            sands = tilt(rocks, sands, size, **tiltargs)
        # M.debug('cycle %s:\n%s', cycle, display(rocks, sands))

        cycle += 1
        if sands in cache:
            prevcycle = cache[sands]
            if cycle + cycle - prevcycle < 1000000000:
                ncycle = (1000000000 - cycle) // (cycle - prevcycle)
                delta = (cycle - prevcycle) * ncycle
                M.debug('current %s, found %s, jump to %s', cycle, prevcycle, cycle + delta)
                cycle += delta
                continue

        cache[sands] = cycle

    print('part2', load(rocks, sands))


if __name__ == '__main__':
    test()
    part1()
    part2()
