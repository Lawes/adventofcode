import pycommon as M
from collections import Counter

cardvalues2 = {k: v for v, k in enumerate('AKQT98765432J')}
cardvalues1 = {k: v for v, k in enumerate('AKQJT98765432')}


def convert_hand1(hand):
    return [cardvalues1[v] for v in hand]


def convert_hand2(hand):
    return [cardvalues2[v] for v in hand]


def load_input(filename, part=1):
    func = convert_hand1 if part == 1 else convert_hand2
    res = []
    with open(filename, 'r') as f:
        for line in f:
            hand, bid = line.split()
            res.append((func(hand), int(bid)))
    return res


def hand_rank(hand):
    values = list(Counter(hand).values())

    c = Counter(values)
    r = 6
    if c[5] == 1:
        r = 0
    elif c[4] == 1:
        r = 1
    elif c[3] == 1 and c[2] == 1:
        r = 2
    elif c[3] == 1:
        r = 3
    elif c[2] == 2:
        r = 4
    elif c[2] == 1:
        r = 5

    return r


def hand_rank_joker(hand):
    try:
        i = hand.index(cardvalues2['J'])
    except ValueError:
        return hand_rank(hand)

    possibles = []
    newhand = hand.copy()
    for k, v in cardvalues2.items():
        if k == 'J':
            continue
        newhand[i] = v
        possibles.append(hand_rank_joker(newhand))
    return min(possibles)


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    for h, b in data:
        print(h, b, hand_rank(h))

    ranked = [(hand_rank(hand), *hand, bid) for hand, bid in data]
    ranked.sort(reverse=True)
    print(ranked)

    print(hand_rank_joker(convert_hand2("KTJJT")))


@M.timeperf
def part1():
    data = load_input('input')
    ranked = [(hand_rank(hand), *hand, bid) for hand, bid in data]
    ranked.sort(reverse=True)
    total = sum([(iv+1) * v[-1] for iv, v in enumerate(ranked)])
    print('part1', total)


@M.timeperf
def part2():
    data = load_input('input', part=2)
    ranked = [(hand_rank_joker(hand), *hand, bid) for hand, bid in data]
    ranked.sort(reverse=True)
    total = sum([(iv+1) * v[-1] for iv, v in enumerate(ranked)])
    print('part2', total)


if __name__ == '__main__':
    test()
    part1()
    part2()
