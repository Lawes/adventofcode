import numpy as np


def conv(c):
    return ord(c) - ord('a')


def load_input(filename):
    grid = []
    start, end = None, None
    with open(filename, 'r') as f:
        for irow, line in enumerate(f):
            row = []
            for icol, c in enumerate(line.strip()):
                if c == 'S':
                    start = (irow, icol)
                    c = 'a'
                elif c == 'E':
                    end = (irow, icol)
                    c = 'z'
                row.append(conv(c))
            grid.append(row)
    return np.array(grid, dtype=int), start, end


class BaseGrid:
    def __init__(self, g):
        self.grid = g
        self.nx, self.ny = g.shape

    def max_cost(self):
        return self.nx * self.ny

    def iter_moves(self, x0, y0):
        raise NotImplementedError()

    def dijkstra(self, x0, y0):
        # x: row
        # y: col
        m = self.max_cost()

        cost = []
        for _ in range(self.nx):
            row = []
            for _ in range(self.ny):
                row.append([m, None])
            cost.append(row)

        lclose = np.zeros_like(self.grid)
        lopen = set([(x0, y0), ])

        cost[x0][y0][0] = 0

        while len(lopen) > 0:
            x, y = min(lopen, key=lambda x: cost[x[0]][x[1]][0])
            lopen.remove((x, y))

            cost_path = cost[x][y][0]
            lclose[x, y] = 1

            for xx, yy in self.iter_moves(x, y):
                if lclose[xx, yy] == 1:
                    continue

                ncost = cost_path + 1
                if ncost < cost[xx][yy][0]:
                    cost[xx][yy] = [ncost, (x, y)]

                if lclose[xx, yy] == 0:
                    lopen.add((xx, yy))

        return cost


class Part1Grid(BaseGrid):
    def iter_moves(self, x0, y0):
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            xx = x0 + dx
            yy = y0 + dy

            if xx >= self.nx or xx < 0 or yy >= self.ny or yy < 0:
                continue

            if self.grid[xx, yy] > self.grid[x0, y0] + 1:
                continue
            yield xx, yy


class Part2Grid(BaseGrid):
    def iter_moves(self, x0, y0):
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            xx = x0 + dx
            yy = y0 + dy

            if xx >= self.nx or xx < 0 or yy >= self.ny or yy < 0:
                continue

            if self.grid[xx, yy] + 1 < self.grid[x0, y0]:
                continue
            yield xx, yy


if __name__ == '__main__':
    grid, s, e = load_input('input')

    # print(grid)
    print(s, e)

    G = Part1Grid(grid)
    c = G.dijkstra(s[0], s[1])
    print('part1', c[e[0]][e[1]])

    nx, ny = grid.shape
    apos = []
    for iy in range(ny):
        for ix in range(nx):
            if grid[ix, iy] == 0:
                apos.append((ix, iy))

    G = Part2Grid(grid)
    c = G.dijkstra(e[0], e[1])
    # print(apos)
    cost = [c[x][y] for x, y in apos]

    print('part2', min(cost))
