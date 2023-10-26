import numpy as np


def load_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    ny = len(lines[0].strip())
    nx = len(lines)

    m = np.zeros((nx, ny))

    for i, row in enumerate(lines):
        m[i, :] = [int(h) for h in row.strip()]

    return m



def bassin_region(data, x0, y0):
    mask = np.zeros_like(data)
    mask[data == 9] = 1

    tocheck = [(x0, y0)]
    mask[x0][y0] = 1

    bassin = [(x0, y0)]

    while len(tocheck) > 0:
        x, y = tocheck.pop()
        v = data[x][y]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xx = x + dx
            if xx >= nx or xx < 0:
                continue
            yy = y + dy
            if yy >= ny or yy < 0:
                continue

            if mask[xx][yy] == 1:
                continue

            if data[xx][yy] > v:
                bassin.append((xx, yy))
                mask[xx][yy] = 1
                tocheck.append((xx, yy))
    return bassin


if __name__ == '__main__':
    data = load_input('input')

    print(data)

    nx, ny = data.shape

    minima = []
    bassin_size = []

    for x in range(nx):
        for y in range(ny):
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                xx = x + dx
                if xx >= nx or xx < 0:
                    continue
                yy = y + dy
                if yy >= ny or yy < 0:
                    continue
                neighbors.append(data[xx][yy])
            if data[x][y] < min(neighbors):
                minima.append(data[x][y])
                bassin = bassin_region(data, x, y)
                bassin_size.append(len(bassin))
#                 print(x, y, len(bassin))

    print(minima)
    bassin_size.sort()

    print('result', np.sum(np.array(minima)+1))

    print('result', np.product(bassin_size[-3:]))