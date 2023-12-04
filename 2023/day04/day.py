import pycommon as M


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            cards = line.split(':')[1]
            winning, youhave = cards.split('|')
            res.append((
                set([int(v) for v in winning.split()]),
                set([int(v) for v in youhave.split()])
            ))
    return res


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    score = 0
    for c in data:
        n = len(c[0] & c[1])
        M.debug(n)
        if n > 0:
            score += pow(2, n-1)
    print(score)


@M.timeperf
def part1():
    data = load_input('input')
    score = 0
    for c in data:
        n = len(c[0] & c[1])
        if n > 0:
            score += pow(2, n-1)
    print('part1', score)


@M.timeperf
def part2():
    data = load_input('input')
    jeuxagratter = [1] * len(data)
    for ic, c in enumerate(data):
        n = len(c[0] & c[1])
        if n > 0:
            for di in range(1, n + 1):
                jeuxagratter[ic + di] += jeuxagratter[ic]
    print('part2', sum(jeuxagratter))


if __name__ == '__main__':
    test()
    part1()
    part2()
