import pycommon as M


class Path(M.AocDijkstra):
    def __init__(self, grid):
        self.G = grid
        x, y = list(zip(*list(grid.keys())))
        self.end = max(x), max(y)

    def is_end(self, state):
        return (state[0], state[1]) == self.end

    def get_voisins(self, state):
        x, y, dir, c = state
        res = []
        for dx, dy in M.DIRECTIONS4:
            if dir == (-dx, -dy):
                continue
            xx, yy = x + dx, y + dy

            if (xx, yy) not in self.G:
                continue

            if dir == (dx, dy):
                if c == 3:
                    continue
                else:
                    nc = c + 1
            else:
                nc = 1
            res.append(((xx, yy, (dx, dy), nc), self.G[(xx, yy)]))
        return res


class Path2(M.AocDijkstra):
    def __init__(self, grid):
        self.G = grid
        x, y = list(zip(*list(grid.keys())))
        self.end = max(x), max(y)

    def is_end(self, state):
        return (state[0], state[1]) == self.end and state[3] >= 4

    def get_voisins(self, state):
        x, y, dir, c = state
        res = []
        for dx, dy in M.DIRECTIONS4:
            if dir == (-dx, -dy):
                continue

            if dir != (0, 0) and c < 4 and dir != (dx, dy):
                continue

            xx, yy = x + dx, y + dy

            if (xx, yy) not in self.G:
                continue

            if dir == (dx, dy):
                if c == 10:
                    continue
                else:
                    nc = c + 1
            else:
                nc = 1
            res.append(((xx, yy, (dx, dy), nc), self.G[(xx, yy)]))
        return res


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
    M.nolog()
    grid, _, _ = M.grid_file('input_test', {str(v): v for v in range(10)})

    print('* normal')
    p = Path(grid)
    print(p.end)
    cost, end_state = p.search((0, 0, (0, 0), 0))
    print(cost)
    path = p.find_path(end_state)
    display([(s[0], s[1]) for s in path])

    print('* ultra crucible')
    p = Path2(grid)
    print(p.end)
    cost, end_state = p.search((0, 0, (0, 0), 0))
    print(cost)
    path = p.find_path(end_state)
    display([(s[0], s[1]) for s in path])


@M.timeperf
def part1():
    M.nolog()
    grid, _, _ = M.grid_file('input', {str(v): v for v in range(10)})

    p = Path(grid)
    print(p.end)
    cost, end_state = p.search((0, 0, (0, 0), 0))
    print('part1', cost)


@M.timeperf
def part2():
    M.nolog()
    grid, _, _ = M.grid_file('input', {str(v): v for v in range(10)})

    p = Path2(grid)
    cost, end_state = p.search((0, 0, (0, 0), 1))
    print('part2', cost)


if __name__ == '__main__':
    test()
    part1()
    part2()
