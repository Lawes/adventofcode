import pycommon as M
import numpy as np


def load_input(filename):
    return M.ints_file(filename)


def prediction(array):
    a = np.array(array)
    last = [array[-1]]
    first = [array[0]]
    while np.any(a != 0):
        a = np.diff(a)
        last.append(a[-1])
        first.append(a[0])

    res = 0
    for e in first[::-1]:
        res = e - res
    M.debug('%s = %s, %s', array, res, sum(last))

    return res, sum(last)


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    for line in data:
        print(prediction(line))


@M.timeperf
def part1():
    M.nolog()
    data = load_input('input')
    total = sum([prediction(line)[1] for line in data])
    print('part1', total)


@M.timeperf
def part2():
    data = load_input('input')
    total = sum([prediction(line)[0] for line in data])
    print('part2', total)


if __name__ == '__main__':
    test()
    part1()
    part2()
