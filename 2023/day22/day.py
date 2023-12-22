import pycommon as M
from collections import defaultdict


def load_input(filename):
    points = M.ints_file(filename)
    points.sort(key=lambda x: min(x[2], x[5]))

    res = []
    for pt in points:
        res.append([
            (x, y, z)
            for x in range(pt[0], pt[3] + 1)
            for y in range(pt[1], pt[4] + 1)
            for z in range(pt[2], pt[5] + 1)
        ])

    return res


def onepiece_falling(ip, piece, ground):
    p = piece
    while True:
        base = []
        onground = False
        newp = [(p[0], p[1], p[2] - 1) for p in p]
        for pt in newp:
            if (v := ground.get(pt, -1)) >= 0 and v != ip:
                base.append(ground[pt])
            elif pt[2] <= 0:
                base.append(-1)
                onground = True
        if onground or base:
            break
        p = newp
    return p, set(base)


def all_falling(pieces):
    is_base_for = defaultdict(set)
    is_supported_by = defaultdict(set)
    ground = {}
    for ip in range(len(pieces)):
        for pt in pieces[ip]:
            ground[pt] = ip

    for step in range(len(pieces)):
        for ip in range(step, len(pieces)):
            newp, base = onepiece_falling(ip, pieces[ip], ground)
            for pt in pieces[ip]:
                del ground[pt]
            pieces[ip] = newp
            for pt in pieces[ip]:
                ground[pt] = ip

    for ip in range(len(pieces)):
        p, base = onepiece_falling(ip, pieces[ip], ground)
        is_supported_by[ip] |= base
        for name in base:
            is_base_for[name].add(ip)
    return ground, is_base_for, is_supported_by


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    print(data)
    ground, base_tree, support_tree = all_falling(data)
    print('base', base_tree)
    print('support on', support_tree)
    for ip in support_tree:
        if len(base_tree[ip]) == 0:
            print(ip)
        elif all(len(support_tree[above]) > 1 for above in base_tree[ip]):
            print(ip)


@M.timeperf
def part1():
    data = load_input('input')
    _, base_tree, support_tree = all_falling(data)
    count = 0
    for ip in range(len(data)):
        if all(len(support_tree[above]) > 1 for above in base_tree[ip]):
            count += 1

    print('part1', count)


@M.timeperf
def part2():
    data = load_input('input')
    _, _, support_tree = all_falling(data)

    total = 0
    for ip in range(len(data)):
        disintegrated = set([ip])

        removed = True
        while removed:
            removed = False
            for ii in range(len(data)):
                if ii in disintegrated:
                    continue
                if len(support_tree[ii] - disintegrated) == 0:
                    disintegrated.add(ii)
                    removed = True

        total += len(disintegrated) - 1
    print('part2', total)


if __name__ == '__main__':
    test()
    part1()
    part2()
