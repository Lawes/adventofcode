

def load_input(filename):
    with open(filename, 'r') as f:
        data = [line.split() for line in f.read().splitlines()]
    return data


_youwin = {
    ('A', 'X'): 1,
    ('A', 'Y'): 2,
    ('B', 'Y'): 1,
    ('B', 'Z'): 2,
    ('C', 'X'): 2,
    ('C', 'Z'): 1
}

_score = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

_goodplay = {
    ('A', 'X'): 'Z',
    ('A', 'Y'): 'X',
    ('A', 'Z'): 'Y',
    ('B', 'X'): 'X',
    ('B', 'Y'): 'Y',
    ('B', 'Z'): 'Z',
    ('C', 'X'): 'Y',
    ('C', 'Y'): 'Z',
    ('C', 'Z'): 'X'
}


def score_turn1(opponent, yourplay):
    k = (opponent, yourplay)
    return _youwin.get(k, 0) * 3 + _score[yourplay]


def score_turn2(opponent, status):
    k = (opponent, status)
    return _score[_goodplay[k]] + (_score[status]-1) * 3


if __name__ == '__main__':
    strategy = load_input('input')

    print('part1', sum(score_turn1(*turn) for turn in strategy))
    print('part1', sum(score_turn2(*turn) for turn in strategy))
