import numpy as np


def load_input(filename):
    with open(filename, 'r') as f:
        data = [int(e) for e in f.readlines()]
    return data


def part1(records):
    test = records[1:] > records[:-1]

    print(sum(test))


def part2(records):
    r1 = records[:-2]
    r2 = records[1:-1]
    r3 = records[2:]

    s = r1 + r2 + r3

    test = s[1:] > s[:-1]

    print(sum(test))



if __name__ == '__main__':
    records = np.array(load_input('input'))

    part1(records)
    part2(records)
