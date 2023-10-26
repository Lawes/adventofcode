import numpy as np
import itertools


def load_input(filename):
    scanners = []
    current = None
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('---'):
                if current is not None:
                    scanners.append(current)
                current = {'x': [], 'y': [], 'z': []}
            elif len(line) > 2:
                pos = [int(e) for e in line.strip().split(',')]
                current['x'].append(pos[0])
                current['y'].append(pos[1])
                current['z'].append(pos[2])

        scanners.append(current)

    for inum, s in enumerate(scanners):
        s['id'] = inum
        s['ref'] = inum
        s['pos'] = np.array([0, 0, 0], dtype=int)
        nprobe = len(s['x'])
        a = np.zeros((nprobe, 3), dtype=int)
        a[:, 0] = s['x']
        a[:, 1] = s['y']
        a[:, 2] = s['z']
        s['m'] = a

    return scanners


def create_sparce(pos):
    return set(((x, y, z) for x, y, z in zip(pos[:, 0], pos[:, 1], pos[:, 2])))


def create_matrice(indices):
    size = 1000
    n = 2*size + 1
    A = np.zeros((n, n, n), dtype=int)

    x = indices[:, 0] + size
    y = indices[:, 1] + size
    z = indices[:, 2] + size
    A[x, y, z] = 1

    print(np.sum(A, axis=(0, 1)))

    return A


x = np.array([1, 0, 0], dtype=int)
y = np.array([0, 1, 0], dtype=int)
z = np.array([0, 0, 1], dtype=int)

transformations = []
for a3, a1 in [
        (x, y), (x, -y), (x, z), (x, -z),
        (y, x), (y, -x), (y, z), (y, -z),
        (z, y), (z, -y), (z, x), (z, -x)
    ]:
    a2 = -np.cross(a1, a3)
    transformations.append(np.vstack([a1, a2, a3]))
    a2 = -np.cross(a1, -a3)
    transformations.append(np.vstack([a1, a2, -a3]))

print('transformations', len(transformations))


def match(sparce1, m2, dx12, dy12, dz12):
    mm = m2.copy()
    mm[:, 0] += dx12
    mm[:, 1] += dy12
    mm[:, 2] += dz12

    sparce2 = create_sparce(mm)

    return len(sparce1 & sparce2)


def find_correlate(m1, m2):
    sparce1 = create_sparce(m1)

    res = 0, None

    for xref, yref, zref in sparce1:
        #print('* point', xref, yref, zref)
        #print('* test', m2[0])
        for t in transformations:
            tm = np.dot(m2, t)
            for pos in tm:

                x2, y2, z2 = pos
                dx, dy, dz = xref - x2, yref - y2, zref - z2
                #print(tm[0], dx, dy, dz)

                m = match(sparce1, tm, dx, dy, dz)
                if m > res[0]:
                    res = m, t, np.array([dx, dy, dz], dtype=int)
                    if m >= 12:
                        return res

    return res


def distance_manhattan(p1, p2):
    return np.abs(p1 - p2).sum()


if __name__ == '__main__':

    data = load_input('input')
    print('num sanners', len(data))
    print(find_correlate(data[0]['m'], data[1]['m']))

    print('part1')

    tocheck = [0]

    while len(tocheck) > 0:
        idata = tocheck.pop()

        ref = data[idata]
        if ref['ref'] != 0:
            continue
        for idata2 in range(len(data)):
            if idata2 == idata:
                continue
            comp = data[idata2]

            if comp['ref'] == 0:
                continue

            corr = find_correlate(ref['m'], comp['m'])
            if corr[0] >= 12:
                print('find correlation', ref['id'], idata2)
                tocheck.append(idata2)

                comp['ref'] = ref['ref']

                comp['pos'] = np.dot(comp['pos'], corr[1]) + corr[2]

                comp['m'] = np.dot(comp['m'], corr[1])
                for i in [0, 1, 2]:
                    comp['m'][:, i] += corr[2][i]


    allpos = set()

    for d in data:
        if d['ref'] != 0:
            raise ValueError('pb ref')
        print('*', d['id'], d['ref'])
        print('pos', d['pos'])
        allpos.update(create_sparce(d['m']))

    print(len(allpos))


    print('part2')

    print(max([distance_manhattan(s1['pos'], s2['pos']) for s1, s2 in itertools.combinations(data, 2)]))
