import pycommon as M

colors = {
    'blue': 0,
    'red': 1,
    'green': 2
}


def load_input(filename):
    games = {}
    with open(filename, 'r') as f:
        for line in f:
            game, sets = line.split(':')
            idgame = int(game.split()[-1])
            sets = sets.split(';')
            conv_sets = []
            for s in sets:
                reveal = [0, 0, 0]
                cubes = s.split(',')
                for c in cubes:
                    for col, icol in colors.items():
                        if col in c:
                            reveal[icol] = int(c.split()[0])
                conv_sets.append(reveal)
            games[idgame] = conv_sets
    return games


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    okgames = []
    for idgame, game in data.items():
        isok = True
        for g in game:
            isok &= g[0] <= 14 and g[1] <= 12 and g[2] <= 13
        if isok:
            okgames.append(idgame)
    print(sum(okgames))


@M.timeperf
def part1():
    data = load_input('input')
    okgames = 0
    for idgame, game in data.items():
        isok = True
        for g in game:
            isok &= g[0] <= 14 and g[1] <= 12 and g[2] <= 13
        if isok:
            okgames += idgame
    print('part1', okgames)


@M.timeperf
def part2():
    data = load_input('input')
    toadd = 0
    for idgame, game in data.items():
        blue, red, green = list(zip(*game))
        toadd += max(blue) * max(red) * max(green)
    print('part2', toadd)


if __name__ == '__main__':
    test()
    part1()
    part2()
