import numpy as np
from numpy.core.numeric import load

def load_input(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            grid.append([int(e) for e in line.strip()])

    return np.array(grid, dtype=int)



def step(grid):
    flash = np.zeros_like(grid)

    newgrid = grid.copy() + 1

    nx, ny = grid.shape

    while np.any(newgrid > 9):
        x0, y0 = np.nonzero(newgrid > 9)

        x0 = x0[0]
        y0 = y0[0]

        newgrid[x0][y0] = 0
        flash[x0][y0] = 1

        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]:
            xx = x0 + dx
            yy = y0 + dy
            if xx < 0 or xx >= nx or yy < 0 or yy >= ny:
                continue
            
            if flash[xx][yy] == 1:
                continue
            
            newgrid[xx][yy] += 1
    return newgrid



if __name__ == '__main__':
    grid = load_input('input')

    print(grid)
    n = 100
    flashcount = 0
    for s in range(n):
        print('step', s+1)
        grid = step(grid)
        flashcount += np.count_nonzero(grid == 0)
        # print(grid)

    print('part1', flashcount)

    grid = load_input('input')
    s = 0
    while True:
        grid = step(grid)
        s += 1
        if np.count_nonzero(grid == 0) == grid.size:
            break
    print(s)