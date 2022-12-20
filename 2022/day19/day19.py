import re
import math
import time


ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

ALL = [ORE, CLAY, OBSIDIAN, GEODE]

_npattern = re.compile(r'-?\d+')


def load_input(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            costs = [int(e) for e in _npattern.findall(line)]
            data.append({
                ORE: (costs[1], 0, 0, 0),
                CLAY: (costs[2], 0, 0, 0),
                OBSIDIAN: (costs[3], costs[4], 0, 0),
                GEODE: (costs[5], 0, costs[6], 0)})
    return data


def explore(bp, maxrobots, minerais, robots, remainingturns, cache):
    if remainingturns == 0:
        return minerais[GEODE]

    state = tuple([*minerais, *robots, remainingturns])

    if state in cache:
        return cache[state]

    maxgeodes = minerais[GEODE] + remainingturns * robots[GEODE]
    if robots[ORE] >= bp[GEODE][ORE] and robots[OBSIDIAN] >= bp[GEODE][OBSIDIAN]:
        n = maxgeodes + remainingturns * (remainingturns + 1) / 2
        cache[state] = n
        return n

    # print('* Explore', remainingturns, minerais, robots)

    for ir, costs in bp.items():

        if robots[ir] >= maxrobots[ir]:
            continue

        # check to bbuild robot ir
        isImpossible = False
        dt = 0
        # print('try to build', ir, costs)
        for imaterial, c in enumerate(costs):
            if c == 0:
                continue
            if robots[imaterial] == 0:
                isImpossible = True
                break
            dt = max(dt, math.ceil(float(c - minerais[imaterial]) / robots[imaterial]))
        # print('to build', ir, isImpossible, dt)
        if isImpossible:
            continue

        # 1 min to build
        dt += 1

        newtime = remainingturns - dt
        if newtime < 0:
            continue

        newmaterials = [
            minerais[im] + robots[im] * dt - costs[im] for im in ALL
        ]

        # limit useless material -> improve cache efficiency
        for im in ALL[:3]:
            newmaterials[im] = min(newmaterials[im], maxrobots[im] * (dt + 1))

        newrobots = robots[:]
        newrobots[ir] += 1

        maxgeodes = max(maxgeodes, explore(bp, maxrobots, newmaterials, newrobots, newtime, cache))

    cache[state] = maxgeodes

    return maxgeodes


def test():
    blueprints = load_input('input_test')
    print(blueprints)

    bp = blueprints[1]
    minerais = [0, 0, 0, 0]
    robots = [1, 0, 0, 0]

    maxrobots = [
        max(bp[t][m] for t in bp) for m in ALL
    ]
    maxrobots[GEODE] = 32
    print(maxrobots)
    print(explore(bp, maxrobots, minerais, robots, maxrobots[GEODE], {}))


def part1():
    blueprints = load_input('input')
    print(blueprints)

    total = 0
    for ibp, bp in enumerate(blueprints):
        tick = time.time()
        minerais = [0, 0, 0, 0]
        robots = [1, 0, 0, 0]

        maxrobots = [
            max(bp[t][m] for t in bp) for m in ALL
        ]
        maxrobots[GEODE] = 24
        maxgeodes = explore(bp, maxrobots, minerais, robots, 24, {})
        print(f'- {ibp:2} = {maxgeodes} in {time.time() - tick:.1f}')

        total += maxgeodes * (ibp + 1)

    print('part1', total)


def part2():
    blueprints = load_input('input')
    print(blueprints)

    total = 1
    for ibp, bp in enumerate(blueprints[:3]):
        tick = time.time()
        minerais = [0, 0, 0, 0]
        robots = [1, 0, 0, 0]

        maxrobots = [
            max(bp[t][m] for t in bp) for m in ALL
        ]
        maxrobots[GEODE] = 32
        maxgeodes = explore(bp, maxrobots, minerais, robots, 32, {})
        print(f'- {ibp:2} = {maxgeodes} in {time.time() - tick:.1f}')

        total *= maxgeodes

    print('part2', total)


if __name__ == '__main__':
    part2()
