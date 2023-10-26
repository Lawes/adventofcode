import numpy as np


def load_input(filename):
    x, y = [], []
    fold = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('fold'):
                equal = line.split()[2]
                var, val = equal.split('=')
                fold.append((var, int(val)))

            else:
                xtxt, ytxt = line.split(',')
                x.append(int(xtxt))
                y.append(int(ytxt))

    nx = np.max(x)+1
    ny = np.max(y)+1

    g = np.zeros((nx, ny), dtype=int)

    for gx, gy in zip(x, y):
        g[gx, gy] = 1
    return g, fold


def fold(grid, pos):
    nx, ny = grid.shape

    newx = max(pos, nx-pos-1)

    ngrid = np.zeros((newx, ny), dtype=int)

    if pos > nx - pos -1:
        ngrid[:nx - pos -1, :] = grid[pos+1:, :]
        ngrid = np.flipud(ngrid)
        ngrid += grid[:pos, :]
    else:
        ngrid[:nx - pos -1, :] = grid[:pos, :]
        ngrid += np.flipud(grid[pos+1:, :])

    return ngrid


if __name__ == '__main__':

    grid, actions = load_input('input')

    for axe, pos in actions:
        if axe == 'x':
            grid = fold(grid, pos)
        else:
            grid = fold(grid.T, pos).T
    
    grid[grid > 0] = 1
    for row in grid.T:
        print(''.join(['.' if e == 0 else '#' for e in row]))

    print(np.count_nonzero(grid))

