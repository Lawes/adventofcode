from collections import defaultdict
import pycommon as M


def load_input(filename):
    with open(filename, 'r') as f:
        grid = set()
        for irow, row in enumerate(f):
            for icol, val in enumerate(row):
                if val == '#':
                    grid.add((icol, irow))
    return grid


_all = [(1, -1), (0, -1), (-1, -1), (1, 1), (0, 1), (-1, 1), (1, 0), (-1, 0)]
_check = {
    'north': [1, 0, 2],
    'south': [4, 5, 3],
    'west': [7, 2, 5],
    'east': [6, 0, 3]
}


def step(grid, direction_order):
    allprop = defaultdict(list)
    static = set()

    for xe, ye in grid:

        check = [(xe + dx, ye + dy) not in grid for dx, dy in _all]
        M.debug("pt %s : %s", (xe, ye), check)
        if all(check):
            M.debug('add static')
            static.add((xe, ye))
        else:
            finddir = False
            for dir in direction_order:

                if all(check[i] for i in _check[dir]):
                    M.debug('find dir %s', dir)
                    finddir = True
                    dx, dy = _all[_check[dir][0]]
                    M.debug('add prop %s', (xe + dx, ye + dy))
                    allprop[(xe + dx, ye + dy)].append((xe, ye))
                    break
            if not finddir:
                M.debug('add static')
                static.add((xe, ye))

    hasmoved = False
    newgrid = static
    for prop, lofelves in allprop.items():
        if len(lofelves) == 1:
            newgrid.add(prop)
            hasmoved = True
        else:
            newgrid.update(lofelves)

    return newgrid, hasmoved


def display(grid, rrange, crange):
    g = [[0] * (crange[1] - crange[0]) for _ in range(rrange[1] - rrange[0])]
    for pt in grid:
        g[pt[1] - rrange[0]][pt[0] - crange[0]] = 1

    for row in g:
        print(''.join('.' if c == 0 else '#' for c in row))


@M.timeperf
def test():
    M.log()
    grid = load_input('input_test')
    display(grid, [-5, 10], [-5, 10])
    direction_order = ['north', 'south', 'west', 'east']
    for _ in range(1):
        M.debug(direction_order)
        grid, _ = step(grid, direction_order)
        direction_order = direction_order[1:] + [direction_order[0]]
        display(grid, [-5, 10], [-5, 10])

    allx, ally = zip(*list(grid))
    print((max(allx) - min(allx) + 1) * (max(ally) - min(ally) + 1) - len(allx))


@M.timeperf
def part1():
    grid = load_input('input')
    direction_order = ['north', 'south', 'west', 'east']
    for _ in range(10):
        grid, _ = step(grid, direction_order)
        direction_order = direction_order[1:] + [direction_order[0]]
    allx, ally = zip(*list(grid))

    print('part1', (max(allx) - min(allx) + 1) * (max(ally) - min(ally) + 1) - len(allx))


@M.timeperf
def part2():
    grid = load_input('input')
    direction_order = ['north', 'south', 'west', 'east']
    hasmoved = True
    count = 0
    while hasmoved:
        grid, hasmoved = step(grid, direction_order)
        count += 1
        direction_order = direction_order[1:] + [direction_order[0]]

    print('part2', count)


if __name__ == '__main__':
    part2()