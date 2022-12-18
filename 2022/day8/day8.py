import numpy as np
from itertools import product


def load_input(filename):
    with open(filename, 'r') as f:
        res = []
        for line in f:
            res.append([int(c) for c in line.strip()])
    return np.array(res, dtype=int)


def indice_visible_array(v):
    prev_max = -1
    visible = []
    for i in range(len(v)):
        if v[i] > prev_max:
            visible.append(i)
            prev_max = v[i]
    return visible


def indice_visible(g):
    nrows, ncols = g.shape

    visible = set()

    for i in range(nrows):
        for indice in indice_visible_array(g[i, :]) + [nrows-e-1 for e in indice_visible_array(g[i, ::-1])]:
            visible.add((i, indice))

    for i in range(ncols):
        for indice in indice_visible_array(g[:, i]) + [ncols-e-1 for e in indice_visible_array(g[::-1, i])]:
            visible.add((indice, i))

    return list(visible)


def count_visible_array(v):
    prev_max = v[0]
    visible = 0
    for i in range(1, len(v)):
        visible += 1
        if v[i] >= prev_max:
            break
    return visible


def scenic_score(ir, jc, g):
    nrows, ncols = g.shape

    left = g[ir, :jc+1][::-1]
    right = g[ir, jc:]
    top = g[:ir+1, jc][::-1]
    down = g[ir:, jc]

    # print('left', left, count_visible_array(left))
    # print('right', right, count_visible_array(right))
    # print('top', top, count_visible_array(top))
    # print('down', down, count_visible_array(down))

    return count_visible_array(left) * count_visible_array(right) * count_visible_array(top) * count_visible_array(down)


if __name__ == '__main__':
    grid = load_input('input_test')

    vgrid = np.zeros_like(grid)

    print(grid[0], indice_visible_array(grid[0]))
    print(grid[0, ::-1], indice_visible_array(grid[0, ::-1]))

    for ir, ic in indice_visible(grid):
        vgrid[ir, ic] = 1

    print(grid)
    print(vgrid)

    print(scenic_score(3, 2, grid))

    grid = load_input('input')
    print('part1', len(indice_visible(grid)))

    nrows, ncols = grid.shape
    print(
        'part2',
        max(
            scenic_score(ir, ic, grid)
            for (ir, ic) in product(range(nrows), range(ncols)))
    )
