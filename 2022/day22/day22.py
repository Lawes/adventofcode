import re
import pycommon as P


_dirs = {
    0: (1, 0),
    2: (-1, 0),
    3: (0, -1),
    1: (0, 1)
}

_pathpattern = re.compile(r'([LR]|\d+)')


class Board:
    def __init__(self, content):
        self.rows = len(content)
        self.cols = max(len(row) for row in content)
        fill = ' ' * self.cols
        self.g = [(line + fill)[:self.cols] for line in content]

    def goto(self, pos, dir):
        dx, dy = _dirs[dir]
        x, y = pos

        P.debug('goto %s, %s', pos, dir)

        while True:
            x = (x + dx) % self.cols
            y = (y + dy) % self.rows
            P.debug('check %s, %s', x, y)
            if self.g[y][x] != ' ':
                break

        return (x, y), dir, self.g[y][x]


TEST = {
    'file': 'input_test',
    'first': (0, 0, 1),
    'dim': 4,
    'face_coords': [
        (8, 0),
        (0, 4),
        (4, 4),
        (8, 4),
        (8, 8),
        (12, 8)],
    'wrapping': {
        (1, 0): (6, 2, lambda x, y: (x, 3 - y)),
        (1, 1): (4, 1, None),
        (1, 2): (3, 1, lambda x, y: (y, x)),
        (1, 3): (2, 1, lambda x, y: (3 - x, y)),
        (5, 0): (6, 0, None),
        (5, 1): (2, 3, lambda x, y: (3 - x, y)),
        (5, 2): (3, 3, lambda x, y: (3 - y, 3 - x)),
        (5, 3): (4, 3, None),
        (2, 0): (3, 0, None),
        (2, 2): (6, 3, lambda x, y: (3 - y, 3 - x)),
        (3, 0): (4, 0, None),
        (4, 0): (6, 1, lambda x, y: (3 - y, 3 - x)),
    }
}

INPUT = {
    'file': 'input',
    'first': (0, 0, 2),
    'dim': 50,
    'face_coords': [
        (100, 0),
        (50, 0),
        (50, 50),
        (50, 100),
        (0, 100),
        (0, 150)],
    'wrapping': {
        (1, 2): (2, 2, None),
        (2, 1): (3, 1, None),
        (3, 1): (4, 1, None),
        (4, 2): (5, 2, None),
        (5, 1): (6, 1, None),
        (1, 1): (3, 2, lambda x, y: (y, x)),
        (3, 2): (5, 1, lambda x, y: (y, x)),
        (4, 1): (6, 2, lambda x, y: (y, x)),
        (1, 0): (4, 2, lambda x, y: (x, 49 - y)),
        (2, 2): (5, 0, lambda x, y: (x, 49 - y)),
        (2, 3): (6, 0, lambda x, y: (y, x)),
        (1, 3): (6, 3, None)
    }
}


class CubeBoard:
    def __init__(self, content, cfg):
        self.dim = cfg['dim']
        self.rows = len(content)
        self.cols = max(len(row) for row in content)
        fill = ' ' * self.cols
        self.g = [(line + fill)[:self.cols] for line in content]

        self.face_coords = cfg['face_coords']

        self.wrapping = cfg['wrapping']
        toadd = [
            ((t[0], (t[1]+2) % 4), (f[0], (f[1]+2) % 4, t[2])) for f, t in self.wrapping.items()
        ]
        self.wrapping.update(toadd)
        print(self.cols, self.rows, len(self.wrapping))

    def globalcoords(self, x, y, face):
        dx, dy = self.face_coords[face - 1]
        return (x + dx, y + dy)

    def goto(self, pos, dir):
        dx, dy = _dirs[dir]
        x, y, face = pos

        P.debug('goto %s, %s', pos, dir)

        nx = x + dx
        ny = y + dy
        P.debug('check %s, %s', nx, ny)
        if nx < 0 or nx > self.dim - 1 or ny < 0 or ny > self.dim - 1:
            P.debug('face %s, dir %s', face, dir)
            face, dir, wrap = self.wrapping[(face, dir)]
            P.debug('new face %s, dir %s', face, dir)
            if wrap is not None:
                nx, ny = wrap(x, y)
            P.debug('new pos %s, %s', nx, ny)
            nx = nx % self.dim
            ny = ny % self.dim
            P.debug('new pos mod, %s, %s', nx, ny)

        xg, yg = self.globalcoords(nx, ny, face)
        return (nx, ny, face), dir, self.g[yg][xg]


def load_input(filename):
    with open(filename, 'r') as f:
        content = f.read().splitlines()

    path = _pathpattern.findall(content.pop())

    return content, path


def followdir(board, pos, dir, n):
    while n > 0:
        newpos, ndir, c = board.goto(pos, dir)
        if c == '#':
            return pos, dir
        pos = newpos
        dir = ndir
        n -= 1
    return pos, dir


def followpath(path, board, first, dir):
    dir = 0
    pos = first
    for inst in path:
        if inst == 'R':
            dir = (dir + 1) % 4
        elif inst == 'L':
            dir = (dir - 1) % 4
        else:
            pos, dir = followdir(board, pos, dir, int(inst))
    return pos, dir


def test():
    P.log()
    board, path = load_input('input_test')
    board = Board(board)
    print(path)
    for line in board.g:
        print(line)
    first, _, _ = board.goto((0, 0), 0)
    pos, _ = followdir(board, first, 2, 10)
    print(pos)

    print('CUBE')
    CFG = TEST
    board, path = load_input(CFG['file'])
    board = CubeBoard(board, CFG)
    print(board.goto((0, 0, 1), 0))
    print(board.goto((3, 1, 4), 0))
    print(board.goto((2, 0, 6), 3))
    print(board.goto((2, 3, 5), 1))
    print(board.goto((1, 3, 2), 1))
    CFG = INPUT
    board, path = load_input(CFG['file'])
    board = CubeBoard(board, CFG)
    print(board.goto((0, 19, 2), 2))


@P.timeperf
def part1():
    board, path = load_input('input')
    board = Board(board)
    first, _, _ = board.goto((0, 0), 0)
    dir = 0

    pos, dir = followpath(path, board, first, dir)

    print('part1', (pos[1] + 1) * 1000 + (pos[0] + 1) * 4 + dir)


@P.timeperf
def part2():
    CFG = INPUT
    board, path = load_input(CFG['file'])
    board = CubeBoard(board, CFG)
    first = CFG['first']

    dir = 0
    pos, dir = followpath(path, board, first, dir)
    gpos = board.globalcoords(*pos)

    print('part2', (gpos[1] + 1) * 1000 + (gpos[0] + 1) * 4 + dir)


if __name__ == '__main__':
    part1()
    part2()
