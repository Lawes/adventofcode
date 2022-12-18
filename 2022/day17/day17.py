from itertools import cycle


def load_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return data


pattern_rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 1), (1, 0)]
]


class Board:
    def __init__(self, cible):
        self.cible = cible
        self.countrocks = -1
        self.board = set()
        self.board.update((i, 0) for i in range(7))

        self.currentheight = 0
        self.h0 = 0

        self.currentrock = None

        self.cache = {}

    def inprint(self):
        return frozenset((pt[0], self.currentheight - pt[1]) for pt in self.board if self.currentheight - pt[1] < 15)

    # from others
    def inprint2(self):
        h = [0] * 7
        for pt in self.board:
            h[pt[0]] = max(h[pt[0]], pt[1])

        m = max(h)
        return tuple(e - m for e in h)

    def max_height(self):
        return self.currentheight + self.h0

    def new_rocks(self):
        self.countrocks += 1
        dy0 = self.currentheight + 4
        dx0 = 2
        return [(x + dx0, y + dy0) for x, y in pattern_rocks[self.countrocks % len(pattern_rocks)]]

    def apply_wind(self, w, rock):
        if w == '>':
            dx = 1
            if rock[-1][0] == 6:
                return rock
        else:
            if rock[0][0] == 0:
                return rock
            dx = -1
        return [(x + dx, y) for x, y in rock]

    def collision(self, rock):
        return not self.board.isdisjoint(rock)

    def play(self, w, iw):
        if self.currentrock is None:
            self.currentrock = self.new_rocks()

        newpos = self.apply_wind(w, self.currentrock)

        if not self.collision(newpos):
            self.currentrock = newpos

        newpos = [(x, y - 1) for x, y in self.currentrock]

        if self.collision(newpos):
            # print('fixe', list(zip(x, y)))
            self.board.update(self.currentrock)
            for ptx, pty in self.currentrock:
                if pty > self.currentheight:
                    self.currentheight = pty

            state = (iw, self.countrocks % len(pattern_rocks), self.inprint())

            if state in self.cache:
                previous_countrock, previous_height = self.cache[state]

                period = self.countrocks - previous_countrock
                dh = self.currentheight - previous_height

                nperiods = (self.cible - self.countrocks) // period

                self.h0 = nperiods * dh

                self.countrocks += period * nperiods
                print('reste', self.cible - self.countrocks)
                self.cache = {}

            self.cache[state] = (self.countrocks, self.currentheight)

            self.currentrock = None
        else:
            self.currentrock = newpos

        return self.cible <= self.countrocks

    def display(self):
        grid = [[0] * 7 for i in range(11)]
        print(self.board)
        for pt in self.board:
            grid[pt[1]][pt[0]] = 1

        for line in grid[::-1]:
            print(' '.join(str(e) for e in line))


def test():
    wind = load_input('input_test')
    nwind = len(wind)
    wind = cycle(wind)

    board = Board(1)

    board.display()

    for iw, w in enumerate(wind):
        if board.play(w, iw%nwind):
            break

    print(board.max_height())
    board.display()


def part1():
    wind = load_input('input')
    nwind = len(wind)
    wind = cycle(wind)

    board = Board(2022)

    board.display()

    for iw, w in enumerate(wind):
        if board.play(w, iw%nwind):
            break

    print(board.currentheight)
    print('part1', board.max_height())


def part2():
    wind = load_input('input')
    nwind = len(wind)
    wind = cycle(wind)

    board = Board(1000000000000)

    for iw, w in enumerate(wind):
        if board.play(w, iw%nwind):
            break

    print('part2', board.max_height())


if __name__ == '__main__':
    part2()