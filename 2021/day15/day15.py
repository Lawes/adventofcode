import numpy as np


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            res.append([int(e) for e in line.strip()])

    return np.array(res, dtype=int)



def dijkstra(x0, y0, g):
    nx, ny = g.shape

    m = nx * ny * np.max(g)

    cost = []
    for _ in range(ny):
        row = []
        for _ in range(ny):
            row.append([m, None])
        cost.append(row)

    lclose = np.zeros_like(g)
    lopen = set([(x0, y0),])

    cost[x0][y0][0] = g[x0, y0]

    while len(lopen) > 0:
        x, y = min(lopen, key=lambda x: cost[x[0]][x[1]][0])
        lopen.remove((x, y))

        if x == nx -1 and y == ny -1:
            break

        cost_path = cost[x][y][0]
        lclose[x, y] = 1

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            xx = x + dx
            yy = y + dy

            if xx >= nx or xx < 0 or yy >= ny or yy < 0:
                continue

            if lclose[xx, yy] == 1:
                continue

            ncost = cost_path + g[xx, yy]
            if ncost < cost[xx][yy][0]:
                cost[xx][yy] = [ncost, (x, y)]

            if lclose[xx, yy] == 0:
                lopen.add((xx, yy))

    return cost


def construct_cave(grid):
    nx, ny = grid.shape

    cave = np.zeros((nx*5, ny*5), dtype=int)

    for tx in range(5):
        for ty in range(5):
            cave[nx*tx:nx*(tx+1), ny*ty:ny*(ty+1)] = np.remainder(grid+tx+ty-1, 9)+1

    return cave


if __name__ == '__main__':
    grid = load_input('input')

    print(grid)
    c = dijkstra(0, 0, grid)

    nx, ny = grid.shape
    # for ix in range(nx):
    #     print([c[ix][iy]['cost'] for iy in range(ny)])

    print('part1', c[nx-1][ny-1][0] - c[0][0][0])

    cave = construct_cave(grid)
    c = dijkstra(0, 0, cave)

    nx, ny = cave.shape
    # for ix in range(nx):
    #     print([c[ix][iy]['cost'] for iy in range(ny)])

    print('part2', c[nx-1][ny-1][0] - c[0][0][0])

