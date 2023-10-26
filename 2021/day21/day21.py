import itertools
from collections import Counter, defaultdict


def move(start, d):
    return ((start-1 + d) % 10) + 1



class DeterministicDice:
    def __init__(self):
        self.nextval = 1
        self.count = 0

    def roll(self):
        res = self.nextval
        self.count += 1
        self.nextval += 1
        if self.nextval > 100:
            self.nextval -= 100
        return res


def part1():
    players = {
        0: {'pos': 6, 'score': 0},
        1: {'pos': 2, 'score': 0}
    }

    d = DeterministicDice()

    curentplayer = 0

    while True:
        dd = d.roll() + d.roll() + d.roll()

        newpos = move(players[curentplayer]['pos'], dd)
        players[curentplayer]['score'] += newpos
        players[curentplayer]['pos'] = newpos
        if players[curentplayer]['score'] >= 1000:
            break
        curentplayer = (curentplayer + 1) % 2


    print(players)
    print('part1', min(players.values(), key=lambda x: x['score'])['score'] * d.count)


possibledd = list([sum(e) for e in itertools.product([1, 2, 3], repeat=3)])


def part2():
    wins = [0, 0]
    univers = {((6, 0), (2, 0)): 1}

    curentplayer = 0

    while len(univers) > 0:
        # print(univers)
        newunivers = defaultdict(int)
        for u, w in univers.items():

            for d in possibledd:
                m = move(u[curentplayer][0], d)
                s = u[curentplayer][1] + m
                if s >= 21:
                    wins[curentplayer] += w
                else:
                    nu = [tuple(u[0]), tuple(u[1])]
                    nu[curentplayer] = (m, s)
                    newunivers[tuple(nu)] += w

        univers = newunivers

        curentplayer = (curentplayer + 1) % 2

    print(wins)



if __name__ == '__main__':

    players = {
        0: {'pos': 4, 'score': 0},
        1: {'pos': 8, 'score': 0}
    }

    # part1()

    part2()
