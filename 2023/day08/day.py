import pycommon as M
import re
from math import lcm


nodepattern = re.compile(r'(\w+) = \((\w+), (\w+)\)')


def load_input(filename):
    nodes = {}
    with open(filename, 'r') as f:
        instructions = next(f).rstrip()
        next(f)
        for line in f:
            m = nodepattern.match(line)
            pere = m.group(1)
            lfils = m.group(2)
            rfils = m.group(3)
            nodes[pere] = {'L': lfils, 'R': rfils}
    return instructions, nodes


def count2end(s, it, nodes, end='ZZZ', it0=0):
    count = 0
    curr = s
    first = True
    while not curr.endswith(end) or first:
        curr = nodes[curr][it[(it0 + count) % len(it)]]
        count += 1
        first = False
    return count, curr


@M.timeperf
def test():
    M.log()
    inst, nodes = load_input('input_test')
    print(inst)


@M.timeperf
def part1():
    inst, nodes = load_input('input')
    print('part1', count2end('AAA', inst, nodes, 'ZZZ')[0])


@M.timeperf
def part2():
    inst, nodes = load_input('input')

    starts = [n for n in nodes if n[-1] == 'A']
    cycles = []

    for s in starts:
        c1, e = count2end(s, inst, nodes, 'Z')
        # look at the second ends
        c2, ee = count2end(e, inst, nodes, 'Z', it0=c1)
        # just to verify that first cycle has to be taken and not the second
        if e != ee:
            print(s, (c1, e), (c2, ee))
        cycles.append(c1)

    print(cycles)
    print("part2", lcm(*cycles))


if __name__ == '__main__':
    test()
    part1()
    part2()
