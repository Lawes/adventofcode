import pycommon as M


def load_input(filename):
    grid = {}
    with open(filename, 'r') as f:
        content = f.read().splitlines()
        ny = len(content)
        nx = len(content[0])
        for iy, line in enumerate(content):
            for ix, c in enumerate(line):
                if c != '.':
                    grid[(ix, iy)] = c
    return grid, (nx, ny)


_cache = set()
def ray(curx, cury, dirx, diry, grid, size, first=True):
    global _cache
    if first:
        _cache = set()
    nx, ny = size
    energized = set()
    while True:
        M.debug('pt %s, %s', curx, cury)

        if curx < 0 or curx >= nx or cury < 0 or cury >= ny:
            break
        key = (curx, cury, dirx, diry)
        if key in _cache:
            M.debug('loop detected')
            break
        _cache.add(key)
        energized.add((curx, cury))

        val = grid.get((curx, cury))
        if val == '/':
            dirx, diry = (-diry, -dirx)
        elif val == '\\':
            dirx, diry = (diry, dirx)
        elif val == '-' and dirx == 0:
            dirx, diry = 1, 0
            M.debug('new ray')
            energized |= ray(curx-1, cury, -1, 0, grid, size, first=False)
        elif val == '|' and diry == 0:
            dirx, diry = 0, 1
            energized |= ray(curx, cury-1, 0, -1, grid, size, first=False)
        curx += dirx
        cury += diry
    return energized


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
    grid, size = load_input('input_test')
    energized = ray(0, 0, 1, 0, grid, size)

    display(energized)
    print(len(energized))


@M.timeperf
def part1():
    M.nolog()
    grid, size = load_input('input')
    print(size)
    energized = ray(0, 0, 1, 0, grid, size)
    print('part1', len(energized))


@M.timeperf
def part2():
    M.nolog()
    grid, size = load_input('input')

    max_energy = 0
    for x in range(size[0]):
        max_energy = max(max_energy, len(ray(x, 0, 0, 1, grid, size)))
        max_energy = max(max_energy, len(ray(x, size[1] - 1, 0, -1, grid, size)))

    for y in range(size[0]):
        max_energy = max(max_energy, len(ray(0, y, 1, 0, grid, size)))
        max_energy = max(max_energy, len(ray(size[0] - 1, y, -1, 0, grid, size)))

    print('par2', max_energy)


if __name__ == '__main__':
    test()
    part1()
    part2()
