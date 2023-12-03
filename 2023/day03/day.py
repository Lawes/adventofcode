import pycommon as M
from collections import defaultdict


def isempty(c):
    return c == ''


def isnum(c):
    return not isempty(c) and '0' <= c <= '9'


def issympbol(c):
    return not isempty(c) and not isnum(c)


def load_input(filename):
    grid = defaultdict(str)
    with open(filename, 'r') as f:
        for iy, line in enumerate(f):
            for ix, c in enumerate(line.strip()):
                if c != '.':
                    grid[(ix, iy)] = c

    return grid, (ix, iy)


def next_num(state, x0, y0, grid):
    # state: current_num, voisins
    endx = x0 + 1
    if not isnum(grid[(x0, y0)]):
        return state, endx

    current, voisins = state
    current += grid[(x0, y0)]
    for dx, dy in [(-1, -1), (-1, 1), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 1)]:
        xx = x0 + dx
        yy = y0 + dy
        v = grid[(xx, yy)]
        if issympbol(v):
            voisins.append((xx, yy))

    endv = grid[(endx, y0)]
    if isnum(endv):
        return next_num((current, voisins), endx, y0, grid)
    elif issympbol(endv):
        voisins.append((endx, y0))
        endx += 1

    return (current, voisins), endx


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    grid, dim = data
    print(dim)

    nums = []
    for iy in range(dim[1]+1):
        ix = 0
        while ix < dim[0] + 1:
            M.debug('pos %s, %s', ix, iy)
            (current, symb), ix = next_num(('', []), ix, iy, grid)
            M.debug('res %s, %s', current, symb)
            if not isempty(current) and symb:
                nums.append(int(current))
    print(nums)
    print(sum(nums))


@M.timeperf
def part1():
    M.nolog()
    data = load_input('input')
    grid, dim = data

    num = 0
    for iy in range(dim[1]+1):
        ix = 0
        while ix < dim[0] + 1:
            (current, symb), ix = next_num(('', []), ix, iy, grid)
            if not isempty(current) and symb:
                num += int(current)
    print('part1', num)


@M.timeperf
def part2():
    M.nolog()
    data = load_input('input')
    grid, dim = data

    gears = defaultdict(list)
    for iy in range(dim[1]+1):
        ix = 0
        while ix < dim[0] + 1:
            (current, symb), ix = next_num(('', []), ix, iy, grid)
            if not isempty(current) and symb:
                for pos in set(symb):
                    if grid[pos] == '*':
                        gears[pos].append(int(current))

    M.debug('gears %s', gears)
    num = 0
    for pos, voisins in gears.items():
        if len(voisins) == 2:
            num += voisins[0] * voisins[1]

    print('part2', num)


if __name__ == '__main__':
    test()
    part1()
    part2()
