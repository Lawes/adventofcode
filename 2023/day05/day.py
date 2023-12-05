import pycommon as M


def load_input(filename):
    res = {}
    with open(filename, 'r') as f:
        content = f.read()
    lines = content.splitlines()
    initial_seeds = [int(v) for v in lines[0].split()[1:]]
    print(initial_seeds)
    origin, dest = '', ''
    transition = []
    for line in lines[1:]:
        if 'map' in line:
            origin, _, dest = line.split()[0].split('-')
        elif line:
            transition.append([int(v) for v in line.split()])
        else:
            if transition:
                res[origin] = {'dest': dest, 'trans': transition}
                transition = []

    if transition:
        res[origin] = {'dest': dest, 'trans': transition}

    return res, initial_seeds


def transform(num, mappings):
    for m in mappings:
        dd = num - m[1]
        if 0 <= dd < m[2]:
            return m[0] + dd
    return num


def transform_range(r0, n0, ref, rmap, n):
    def f(num):
        return num - ref + rmap

    resid, resf = [], []
    r0e = r0 + n0 - 1
    refe = ref + n - 1
    if r0 < ref:
        if r0e < ref:
            M.debug('1')
            resid.append([r0, n0])
        elif r0e < refe:
            M.debug('2')
            resid.append([r0, ref - r0])
            resf.append([f(ref), r0e - ref + 1])  # tranform
        else:
            M.debug('3')
            resid.append([r0, ref - r0])
            resf.append([f(ref), n])  # tranform
            resid.append([refe + 1, r0e - refe])
    elif r0 > refe:
        M.debug('4')
        resid.append([r0, n0])
    else:
        if r0e <= refe:
            M.debug('5')
            resf.append([f(r0), n0])
        else:
            M.debug('6')
            resf.append([f(r0), refe - r0 + 1])
            resid.append([refe + 1, r0e - refe])
    return resid, resf


def transform_map(r, maps):
    res = []
    cur = [r]
    for m in maps:
        newcur = []
        for e in cur:
            rid, rf = transform_range(e[0], e[1], m[1], m[0], m[2])
            res.extend(rf)
            newcur.extend(rid)
        cur = newcur
    return res + cur


def play(num, data):
    node = 'seed'
    while node != 'location':
        n = data[node]
        num = transform(num, n['trans'])
        node = n['dest']
    return num


def play_range(r, data):
    res = [r]
    node = 'seed'
    while node != 'location':
        n = data[node]
        newres = []
        for e in res:
            newres.extend(transform_map(e, n['trans']))
        res = newres
        node = n['dest']

    return res


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    data, init = data
    print(data)
    print(transform(0, data['seed']['trans']))
    print(transform(50, data['seed']['trans']))
    print(transform(96, data['seed']['trans']))
    print(transform(99, data['seed']['trans']))
    print(transform(100, data['seed']['trans']))
    print(play(79, data))
    print(play(82, data))

    for seed in init:
        print('seed', seed)
        print(play(seed, data))

    print(transform_range(1, 1, 0, 10, 3))
    print(transform_range(2, 2, 0, 10, 3))
    print(transform_range(-1, 3, 0, 10, 3))
    print(transform_range(-1, 5, 0, 10, 3))
    print(transform_range(-2, 2, 0, 10, 3))
    print(transform_range(3, 2, 0, 10, 3))
    M.nolog()
    print(play_range([79, 2], data))


@M.timeperf
def part1():
    M.nolog()
    graph, init = load_input('input')
    locations = [play(seed, graph) for seed in init]
    print('part1', min(locations))


@M.timeperf
def part2():
    graph, init = load_input('input')

    seeds = list(zip(init[0::2], init[1::2]))
    print(seeds)
    locations = []
    for seed in seeds:
        p = play_range(seed, graph)
        locations.extend(p)

    print('part2', min([loc[0] for loc in locations]))


if __name__ == '__main__':
    test()
    part1()
    part2()
