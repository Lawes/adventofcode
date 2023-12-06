import math
import pycommon as M


def load_input(filename):
    content = M.ints_file(filename)
    return content[0], content[1]


def times2win(reftime, mindist):
    delta = reftime * reftime - 4 * mindist
    if delta < 0:
        return 0, 0
    d1 = 0.5 * (reftime - math.sqrt(delta))
    d2 = 0.5 * (reftime + math.sqrt(delta))
    M.debug(f'{d1} {d2}')
    return math.floor(d1 + 1), math.ceil(d2 - 1)


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    games = zip(*data)

    for g in games:
        rt = times2win(g[0], g[1])
        print(rt, rt[1] - rt[0] + 1)


@M.timeperf
def part1():
    M.nolog()
    data = load_input('input')

    n = 1
    for g in zip(*data):
        rt = times2win(g[0], g[1])
        n *= rt[1] - rt[0] + 1
    print('part1', n)


@M.timeperf
def part2():
    time, dist = load_input('input')

    time = int(''.join([str(v) for v in time]))
    dist = int(''.join([str(v) for v in dist]))
    rt = times2win(time, dist)
    print('part2', rt[1] - rt[0] + 1)


if __name__ == '__main__':
    test()
    part1()
    part2()
