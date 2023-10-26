import numpy as np


def load_input(filename):
    with open(filename, 'r') as f:
        line = next(f).rstrip().split(',')
    return np.array([int(p) for p in line], dtype=int)


def cost_p1(p0, crabs):
    return np.sum(np.abs(crabs - p0))


def cost_p2(p0, crabs):
    delta = np.abs(crabs - p0)
    return np.sum(delta * (delta + 1) / 2)
    


if __name__ == '__main__':
    crabs = load_input('input')

    cost = cost_p2

    p0 = int(np.mean(crabs))
    c0 = cost(p0, crabs)

    if c0 > cost(p0 + 1, crabs):
        s = 1
    else:
        s = -1

    while True:
        p1 = p0 + s
        c1 = cost(p1, crabs)

        if c1 > c0:
            break

        p0 = p1
        c0 = c1

    print(p0, c0)
