import pycommon as M


def load_input(filename):
    with open(filename, 'r') as f:
        return M.grid_txt(f.read(), {k: k for k in '#><^v'})


@M.timeperf
def part1():
    grid, nx, ny = load_input('input')
    start = (1, 0)
    end = (nx - 2, ny - 1)

    queue = [(set([start]), start)]

    maxlength = 0

    while queue:
        path, pt = queue.pop()

        if pt == end:
            if (ll := len(path)) > maxlength:
                maxlength = ll
            continue

        directions = M.DIRECTIONS4
        if (v := grid.get(pt, '.')) == '>':
            directions = [(1, 0)]
        elif v == '<':
            directions = [(-1, 0)]
        elif v == 'v':
            directions = [(0, 1)]
        elif v == '^':
            directions = [(0, -1)]

        for dx, dy in directions:
            xx = pt[0] + dx
            yy = pt[1] + dy
            v = grid.get((xx, yy), '.')
            if v == '#' or yy >= ny or yy < 0:
                continue
            if (xx, yy) not in path:
                newpath = path.copy()
                newpath.add((xx, yy))
                queue.append((newpath, (xx, yy)))

    print('part1', maxlength - 1)


@M.timeperf
def part2():
    grid, nx, ny = load_input('input')
    start = (1, 0)
    end = (nx - 2, ny - 1)

    queue = [(set(), start)]

    maxlength = 0

    while queue:
        path, pt = queue.pop()

        if pt == end:
            if (ll := len(path)) > maxlength:
                maxlength = ll
                print(maxlength)
            continue

        while True:
            res = []
            directions = M.DIRECTIONS4
            for dx, dy in directions:
                xx = pt[0] + dx
                yy = pt[1] + dy
                v = grid.get((xx, yy), '.')
                if v == '#' or yy >= ny or yy < 0:
                    continue
                if (xx, yy) not in path:
                    res.append((xx, yy))
            if len(res) == 1:
                path.add(pt)
                pt = res[0]
                if pt == end:
                    queue.append((path.copy(), pt))
                    break

                continue
            for choice in res:
                newpath = path.copy()
                newpath.add(pt)
                queue.append((newpath, choice))
            break

    print('part2', maxlength)


if __name__ == '__main__':
    part1()
    part2()
