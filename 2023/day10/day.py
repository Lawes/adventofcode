from collections import defaultdict
import pycommon as M

pipes = {
    '|': [(0, -1), (0, 1)],
    '-': [(1, 0), (-1, 0)],
    'L': [(0, -1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(0, 1), (-1, 0)],
    'F': [(0, 1), (1, 0)]
}


def load_input(filename):
    grid = defaultdict(str)
    start = None
    with open(filename, 'r') as f:
        for iy, line in enumerate(f):
            for ix, c in enumerate(line):
                if c == 'S':
                    start = (ix, iy)
                elif c in pipes:
                    grid[(ix, iy)] = c

    return grid, start


def get_connection(grid, x0, y0):
    return [(x0 + dx, y0 + dy) for dx, dy in pipes.get(grid[(x0, y0)], [])]


def follow_loop(x0, y0, grid):
    starts = []
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        xx = x0 + dx
        yy = y0 + dy

        for pt in get_connection(grid, xx, yy):
            if pt == (x0, y0):
                starts.append((xx, yy, dx, dy))

    M.debug('starts %s', starts)
    curr = starts[0][:2]
    d1 = starts[0][2:]
    end = starts[1][:2]
    d2 = starts[1][2:]

    for k, d in pipes.items():
        if d1 in d and d2 in d:
            start_pipe = k

    path = set([(x0, y0), curr])
    while curr != end:
        for pt in get_connection(grid, *curr):
            if pt not in path:
                curr = pt
                break
        path.add(curr)

    return path, start_pipe


@M.timeperf
def test():
    M.log()
    grid, start = load_input('input_test')
    print(start)
    path, S = follow_loop(start[0], start[1], grid)
    print(path, len(path), S)


@M.timeperf
def part1():
    grid, start = load_input('input')
    path, S = follow_loop(start[0], start[1], grid)
    print('part1', len(path) // 2)


@M.timeperf
def part2():
    M.nolog()
    grid, start = load_input('input')
    path, S = follow_loop(start[0], start[1], grid)
    grid[start] = S

    x, y = list(zip(*list(path)))
    xrange = [min(x), max(x)]
    yrange = [min(y), max(y)]

    inside = []
    for x in range(xrange[0], xrange[1] +1):
        for y in range(yrange[0], yrange[1] +1):
            pt = (x, y)
            if pt in path:
                continue

            cross = 0
            crosstxt = ''
            M.debug('test inside %s', pt)
            for xx in range(xrange[0], x):
                t = (xx, y)
                v = grid[t]
                if t not in path or v == '':
                    continue
                crosstxt += v
                if v == '|':
                    cross += 2
                elif v in 'L7':
                    cross += 1
                elif v in 'FJ':
                    cross -= 1
            M.debug('    %s -> %s %% 4 = %s', crosstxt, cross, cross % 4)
            if (cross % 4) == 2:
                M.debug('     inside')
                inside.append(pt)

    print('part2', len(inside))


if __name__ == '__main__':
    test()
    part1()
    part2()
