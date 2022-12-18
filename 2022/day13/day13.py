from itertools import chain
import functools
import numpy as np


def load_input(filename):
    with open(filename, 'r') as f:
        content = [eval(e) for e in f.read().splitlines() if e]
    l1 = content[::2]
    l2 = content[1::2]

    return list(zip(l1, l2))


def compare(e1, e2):
    if isinstance(e1, int) and isinstance(e2, int):
        return e1 - e2

    elif isinstance(e1, list) and isinstance(e2, list):
        for ee1, ee2 in zip(e1, e2):
            test = compare(ee1, ee2)
            if test != 0:
                return test
        return len(e1) - len(e2)

    elif isinstance(e1, int):
        return compare([e1], e2)
    elif isinstance(e2, int):
        return compare(e1, [e2])

    return 0


if __name__ == '__main__':
    data = load_input('input')

    count = 0
    for ie, pair in enumerate(data):
        e1, e2 = pair
        if compare(e1, e2) < 0:
            count += ie+1

    print('part1', count)

    allpackets = list(chain(*data))
    allpackets.extend([[[2]], [[6]]])

    allpackets.sort(key=functools.cmp_to_key(lambda x, y: compare(x, y)))

    prod = 1
    print(
        'part2',
        np.prod([
            ip + 1
            for ip, p in enumerate(allpackets)
            if compare(p, [[2]]) == 0 or compare(p, [[6]]) == 0
        ]))
