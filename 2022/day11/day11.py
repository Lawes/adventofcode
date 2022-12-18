import re


pattern_plus = re.compile('new = old + (\d+)')
pattern_mult = re.compile('new = old * (\d+)')


def identify_op(txt):
    op = None
    if txt == 'new = old * old':
        op = lambda x: x*x
    elif txt.startswith('new = old *'):
        v = int(txt.split()[-1])
        op = lambda x: x*v
    elif txt.startswith('new = old +'):
        v = int(txt.split()[-1])
        op = lambda x: x + v
    return op


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        monkey = {}
        for line in f:
            line = line.strip()
            if line.startswith('Monkey'):
                if len(monkey) > 0:
                    res.append(monkey)
                    monkey = {}
            elif line.startswith('Starting items:'):
                monkey['items'] = [int(e.strip()) for e in line.split(':')[1].split(',')]
            elif line.startswith('Test:'):
                monkey['div'] = int(line.split()[-1])
            elif line.startswith('Operation:'):
                monkey['op'] = identify_op(line.split(':')[1].strip())
            elif line.startswith('If true:'):
                monkey['true'] = int(line.split()[-1])
            elif line.startswith('If false:'):
                monkey['false'] = int(line.split()[-1])
        if len(monkey) > 0:
            res.append(monkey)
    return res


def play_onemokey(monkey):
    todo = []
    for item in monkey['items']:
        v = monkey['op'](item)//3

        if v%monkey['div'] == 0:
            todo.append((monkey['true'], v))
        else:
            todo.append((monkey['false'], v))
    monkey['items'] = []
    return todo


def part1():
    monkeys = load_input('input_test')
    print(monkeys)
    count = [0] * len(monkeys)
    for _ in range(20):
        for im, m in enumerate(monkeys):
            count[im] += len(m['items'])
            for dest, v in play_onemokey(m):
                monkeys[dest]['items'].append(v)
    count.sort()
    print(monkeys)
    print('part1', count[-1] * count[-2])


def play_onemokey2(im, monkey):
    todo = []
    for item in monkey['items']:
        vals = [(monkey['op'](v)%d, d) for v, d in item]

        if vals[im][0] == 0:
            todo.append((monkey['true'], vals))
        else:
            todo.append((monkey['false'], vals))
    monkey['items'] = []
    return todo


def part2():
    monkeys = load_input('input')
    count = [0] * len(monkeys)

    alldivs = [m['div'] for m in monkeys]

    for m in monkeys:
        m['items'] = [list(zip([v] * len(monkeys), alldivs)) for v in m['items']]
    print(monkeys)
    for _ in range(10000):
        for im, m in enumerate(monkeys):
            count[im] += len(m['items'])
            for dest, v in play_onemokey2(im, m):
                monkeys[dest]['items'].append(v)
    print(count)
    count.sort()
    print('part2', count[-1] * count[-2])


if __name__ == '__main__':
    part1()
    part2()
