import pycommon as M


def load_input(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            dir, n, color = line.rstrip().split()
            data.append((dir, int(n), color.strip('(#)')))
    return data


def display(points):
    x, y = list(zip(*points))

    xrange = min(x), max(x)
    yrange = min(y), max(y)

    grid = []
    for _ in range(yrange[1] - yrange[0] + 1):
        grid.append(['.'] * (xrange[1] - xrange[0] + 1))

    for pt in points:
        grid[pt[1] - yrange[0]][pt[0] - xrange[0]] = '#'

    for row in grid:
        print(''.join(row))


def trench(data):
    dirname = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0)
    }

    grid = [(0, 0)]
    x, y = 0, 0
    for dir, n, color in data:
        dx, dy = dirname[dir]
        x += dx*n
        y += dy*n
        grid.append((x, y))
    return grid


def correct_data(data):
    mapping = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }
    newdata = []
    for dir, n, color in data:
        newn = int(color[:5], 16)
        newdir = mapping[color[-1]]
        newdata.append((newdir, newn, ''))
    return newdata


def perimeter(g):
    res = 0
    for i in range(len(g) - 1):
        x1, y1 = g[i]
        x2, y2 = g[i+1]

        res += abs(x2 - x1) + abs(y2 - y1)
    return res


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')

    g = trench(data)

    display(g)

    # théorème de Pick, merci aux solutions vues pour le problème 10!
    p = perimeter(g)
    i = M.area_shoelace(g) - p / 2 + 1
    print(i + p)


@M.timeperf
def part1():
    data = load_input('input')

    g = trench(data)
    p = perimeter(g)
    i = M.area_shoelace(g) - p / 2 + 1

    print('part1', i + p)


@M.timeperf
def part2():
    data = load_input('input')
    data = correct_data(data)
    g = trench(data)
    p = perimeter(g)
    i = M.area_shoelace(g) - p / 2 + 1

    print('part2', i + p)



if __name__ == '__main__':
    test()
    part1()
    part2()