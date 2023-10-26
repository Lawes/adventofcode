from collections import defaultdict
import numpy as np

def load_input(filename):
    with open(filename, 'r') as f:
        algo = [int(e == '#') for e in next(f).strip()]

        next(f)

        img = defaultdict(int)

        for ix, line in enumerate(f):
            for iy, v in enumerate(line.strip()):
                if v == '#':
                    pos = (ix, iy)
                    img[pos] = 1

    return img, algo


def bin2num(bintxt):
    val = 0
    for d in bintxt:
        val = 2 * val + d
    return val


class Enhancer:
    def __init__(self, data, algo):
        self.algo = algo
        self.content = data

    def __getitem__(self, key):
        x, y = key

        r = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                r.append(self.content[(x+dx, y+dy)])

        indice = bin2num(r)

        return self.algo[indice]


def double_enhance(img, algo):
    nx, ny = 0, 0

    for pos in img:
        x, y = pos
        nx = max(nx, x)
        ny = max(ny, y)

    s1 = Enhancer(img, algo)
    s2 = Enhancer(s1, algo)

    newimg = defaultdict(int)

    for ix in range(-2, nx+3):
        for iy in range(-2, ny+3):
            if s2[(ix, iy)] == 1:
                newimg[ix + 2, iy + 2] = 1

    return newimg


if __name__ == '__main__':
    img, algo = load_input('input')

    for s in range(25):
        img = double_enhance(img, algo)

    print(len(img))
