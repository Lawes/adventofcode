import numpy as np

def load_input(filename):
    data = []
    maxx = 0
    maxy = 0

    with open(filename, 'r') as f:
        for line in f:
            p1, _, p2 = line.rstrip().split(' ')
            p1 = p1.split(',')
            p2 = p2.split(',')
            x1, y1 = int(p1[0]), int(p1[1])
            x2, y2 = int(p2[0]), int(p2[1])
            maxx = max(max(x1, x2), maxx)
            maxy = max(max(y1, y2), maxy)
            data.append({'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2)})

    return data, maxx+1, maxy+1


def iterator_line(x1, y1, x2, y2):
    if x1 == x2:
        vmin, vmax = min(y1, y2), max(y1, y2)
        for v in range(vmin, vmax + 1):
            yield x1, v
    elif y1 == y2:
        vmin, vmax = min(x1, x2), max(x1, x2)
        for v in range(vmin, vmax + 1):
            yield v, y1
    elif abs(x2 - x1) == abs(y2 - y1):
        delta = abs(x2 - x1)
        sigx = 1 if x2 >= x1 else -1
        sigy = 1 if y2 >= y1 else -1

        for d in range(delta+1):
            yield x1 + sigx*d, y1 + sigy*d


if __name__ == '__main__':
    data, maxx, maxy = load_input('input')

    print(maxx, maxy)
    print(data)

    map = np.zeros((maxx, maxy))

    for pts in data:
        for x, y in iterator_line(pts['x1'], pts['y1'], pts['x2'], pts['y2']):
            map[x][y] += 1

    # print(map)

    mask = map >= 2

    print(np.sum(mask))
