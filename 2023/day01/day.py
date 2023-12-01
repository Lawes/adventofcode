import pycommon as M
import re

numbers = [
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
] + [(str(n), n) for n in range(10)]


def load_input(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content.splitlines()


def numInLine(txt):
    return [c for c in txt if '0' <= c <= '9']


def extractnum(txt):
    res = []
    for numtxt, num in numbers:
        for m in re.finditer(numtxt, txt):
            res.append((m.start(), str(num)))
    if res:
        res.sort()
        res = [e[1] for e in res]

    return res


@M.timeperf
def test():
    M.log()
    print(extractnum('rone'))
    print(extractnum('eightwothree'))
    print(extractnum('4nineeightsevenseven2'))

    data = load_input('input_test')
    s1 = 0
    for il, line in enumerate(data):
        nums = numInLine(line)
        M.debug('line %s %s: %s', il, line, nums)
        s1 += int(nums[0] + nums[-1])

    data = load_input('input_test2')
    s2 = 0
    for il, line in enumerate(data):
        nums = extractnum(line)
        M.debug('line %s %s: %s', il, line, nums)
        s2 += int(nums[0] + nums[-1])
    print(s1, s2)


@M.timeperf
def part1():
    data = load_input('input')
    s = 0
    for line in data:
        nums = numInLine(line)
        s += int(nums[0] + nums[-1])
    print('part1', s)


@M.timeperf
def part2():
    data = load_input('input')
    s = 0
    for line in data:
        nums = extractnum(line)
        s += int(nums[0] + nums[-1])
    print('part2', s)


if __name__ == '__main__':
    test()
    part1()
    part2()
