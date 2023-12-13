import pycommon as M
from itertools import chain


def convert(pattern):
    return [tuple(int(c == '#') for c in line) for line in pattern]


def load_input(filename):
    with open(filename, 'r') as f:
        return [convert(p.splitlines()) for p in f.read().split('\n\n')]


def search_hmirrors(pattern, smudge=False):
    mirrors = []
    for i in range(1, len(pattern)):
        n2cmp = min(i, len(pattern) - i)
        M.debug('* %s, %s', i, n2cmp)
        p1 = chain(*pattern[i-n2cmp:i])
        p2 = chain(*pattern[i:i+n2cmp:][::-1])
        diff = [e1 ^ e2 for e1, e2 in zip(p1, p2)]

        if sum(diff) == int(smudge):
            mirrors.append(i)

    return mirrors


def transpose(pattern):
    return [tuple(p) for p in list(zip(*pattern))]


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    print(data[0])
    print(transpose(data[0]))

    print(search_hmirrors(transpose(data[0])))
    print(search_hmirrors(data[1]))
    print(search_hmirrors(data[0], smudge=True))
    print(search_hmirrors(data[1], smudge=True))


@M.timeperf
def part1():
    M.nolog()
    data = load_input('input')

    s = 0
    for pattern in data:
        s += 100 * sum(search_hmirrors(pattern))
        s += sum(search_hmirrors(transpose(pattern)))

    print('part1', s)


@M.timeperf
def part2():
    M.nolog()
    data = load_input('input')
    s = 0
    for pattern in data:
        s += 100 * sum(search_hmirrors(pattern, smudge=True))
        s += sum(search_hmirrors(transpose(pattern), smudge=True))

    print('part2', s)


if __name__ == '__main__':
    test()
    part1()
    part2()
