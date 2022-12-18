
def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            e1, e2 = line.strip().split(',')
            r1 = [int(v) for v in e1.split('-')]
            r2 = [int(v) for v in e2.split('-')]
            res.append((r1, r2))
    return res


def includein(r1, r2):
    maxr = [
        min(r1[0], r2[0]),
        max(r1[1], r2[1])
    ]
    return maxr == r1 or maxr == r2


def overlap(r1, r2):
    a1, b1 = r1
    a2, b2 = r2
    if b2 >= b1:
        rr1 = (a1, b1)
        rr2 = (a2, b2)
    else:
        rr1 = (a2, b2)
        rr2 = (a1, b1)

    return rr1[1] >= rr2[0]


if __name__ == '__main__':
    data = load_input('input')

    print(
        'part1',
        sum(int(includein(e1, e2)) for e1, e2 in data)
    )

    print(
        'part2',
        sum(int(overlap(e1, e2)) for e1, e2 in data)
    )
