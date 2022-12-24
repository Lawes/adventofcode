import pycommon as M
import heapq


_blizzard = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}


def load_input(filename):
    wind = []
    nr, nc = 0, 0
    with open(filename, 'r') as f:
        for irow, row in enumerate(f):
            nr += 1
            for icol, v in enumerate(row):
                nc = len(row) - 1
                if v in _blizzard:
                    wind.append((icol, irow, v))
    return wind, (nc, nr), (1, 0), (nc - 1, nr - 1)


def wind_forward(wind, size):
    newwind = []
    for x, y, v in wind:
        dx, dy = _blizzard[v]
        x += dx
        y += dy
        if x == size[0]:
            x = 1
        elif x == 0:
            x = size[0] - 1
        if y == size[1] - 1:
            y = 1
        elif y == 0:
            y = size[1] - 2
        newwind.append((x, y, v))
    return newwind


def create_grid(wind, size):
    g = [[' '] * (size[0] + 1) for _ in range(size[1])]
    for x, y, w in wind:
        g[y][x] = w

    return g


def display(wind, size):
    g = create_grid(wind, size)

    for row in g:
        print(''.join('.' if c == ' ' else c for c in row))


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def explore(wind, size, start, end):

    allwinds = [wind]
    allgrids = [create_grid(wind, size)]

    close = set()

    def de(x, y):
        return distance(x, y, end[0], end[1])

    q = [(de(start[0], start[1]), 0, start[0], start[1])]

    mint = 10000000

    while q:
        state = heapq.heappop(q)

        if state[1:] in close:
            continue

        close.add(state[1:])

        M.debug('*state %s', state)
        dend, t, x, y = state
        newt = t + 1

        if newt > mint:
            continue

        while len(allgrids) <= newt:
            w = wind_forward(allwinds[-1], size)
            g = create_grid(w, size)
            allwinds.append(w)
            allgrids.append(g)

        find = False
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            newx = x + dx
            newy = y + dy
            if (newx, newy) == end:
                mint = min(mint, newt)
                print('FIND in', mint)
                find = True
                break

            if 1 <= newx <= size[0] - 1 and 1 <= newy <= size[1] - 2:
                M.debug('check %s, %s with %s', newx, newy, allgrids[newt][newy][newx])
                if allgrids[newt][newy][newx] == ' ':
                    heapq.heappush(q, (de(newx, newy), newt, newx, newy))

        M.debug('check static with %s', allgrids[newt][y][x])
        if not find and allgrids[newt][y][x] == ' ':
            heapq.heappush(q, (dend, newt, x, y))
    return mint


@M.timeperf
def test():
    M.log()
    wind, size, start, out = load_input('input_test')
    print(start)
    display(wind, size)
    w = wind.copy()
    for _ in range(2):
        print('*')
        w = wind_forward(w, size)
        display(w, size)

    for _ in range(18):
        wind = wind_forward(wind, size)
    print('**')
    display(wind, size)
    print(explore(wind, size, out, start))


@M.timeperf
def part1():
    wind, size, start, out = load_input('input')
    print(start)
    mint = explore(wind, size, start, out)
    print('part1', mint)


@M.timeperf
def part2():
    wind, size, start, out = load_input('input')
    print(start)

    mint1 = explore(wind, size, start, out)

    print('step 1', mint1)

    for _ in range(mint1):
        wind = wind_forward(wind, size)
    mint2 = explore(wind, size, out, start)

    print('step 2', mint2)
    for _ in range(mint2):
        wind = wind_forward(wind, size)
    mint3 = explore(wind, size, start, out)

    print('part2', mint1 + mint2 + mint3)


if __name__ == '__main__':
    part2()
