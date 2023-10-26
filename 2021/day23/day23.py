from collections import Counter
import numpy as np


class DoubleDict(object):
    def __init__(self, *args):
        self.dict12 = {}
        self.dict21 = {}
        for pair in args:
            self.dict12[pair[0]] = pair[1]
            self.dict21[pair[1]] = pair[0]

    def in1(self, key):
        return key in self.dict12

    def in2(self, key):
        return key in self.dict21

    def __contains__(self, key):
        return self.in1(key)

    def __getitem__(self, key):
        return self.dict12.get(key) or self.dict21.get(key)


class Labyrinth:
    siderooms = DoubleDict(
        ('A', 2), ('B', 4), ('C', 6), ('D', 8)
    )

    def __init__(self, prof=2):
        self.prof = prof
        self.clear()

    def clear(self):
        self.rooms = {
            'H': ['0', '0', 'x', '0', 'x', '0', 'x', '0', 'x', '0', '0'],
            'A': ['0'] * self.prof,
            'B': ['0'] * self.prof,
            'C': ['0'] * self.prof,
            'D': ['0'] * self.prof
        }

    def checkSideRoom(self, room):
        for v in self.rooms[room]:
            if v != room:
                return False
        return True

    def display(self):
        def txtcontent(v):
            return ' {0} '.format(v if v not in '0x' else '.')
        print('###' * 13)
        row = '###'
        for indice in range(11):
            row += txtcontent(self.rooms['H'][indice])
        print(row + '###')
        for rpos in range(self.prof):
            row = ''
            for indice in range(-1, 12):
                if self.siderooms.in2(indice):
                    row += txtcontent(self.rooms[self.siderooms[indice]][rpos])
                else:
                    row += '###'
            print(row)

    def get(self, room, x):
        return self.rooms[room][x]

    def isFinished(self):
        for room in 'ABCD':
            if not self.checkSideRoom(room):
                return False
        return True

    def isBlocked(self, pos):
        return self.get(**pos) > 0

    def place(self, *players):
        for p in players:
            self.rooms[p['room']][p['x']] = p['name']

    def freeH(self, indice):
        res = []
        siderooms = []
        for onerange in [range(indice-1, -1, -1), range(indice+1, 11)]:
            for ix in onerange:
                v = self.get(room='H', x=ix)
                if v in self.siderooms:
                    break
                elif v == 'x':
                    siderooms.append({'room': self.siderooms[ix], 'step': abs(ix - indice)})
                elif v == '0':
                    res.append({'room': 'H', 'x': ix, 'step': abs(ix - indice)})

        return res, siderooms

    def freeposSideRoom(self, sideroom):
        minpos = -1
        for v in self.rooms[sideroom]:
            if v != '0' and v != sideroom:
                return minpos

        for i in range(self.prof):
            if self.rooms[sideroom][i] != '0':
                return i - 1
        return self.prof - 1

    def explore(self, name, room, x):
        res = []
        if room in self.siderooms:
            for i in range(x - 1, -1, -1):
                if self.get(room, i) != '0':
                    return []
            roomstep = x + 1

            resH, tocheck = self.freeH(self.siderooms[room])
            findOne = False
            for sideroom in tocheck:
                if name == sideroom['room']:
                    pos = self.freeposSideRoom(name)
                    if pos >= 0:
                        res.append({'room': name, 'x': pos, 'step': sideroom['step'] + pos + 1 + roomstep})
                        findOne = True
                    break
            if not findOne:
                for e in resH:
                    e['step'] += roomstep
                res.extend(resH)

        else:
            resH, tocheck = self.freeH(x)
            # res.extend(resH)
            for sideroom in tocheck:
                if name == sideroom['room']:
                    pos = self.freeposSideRoom(name)
                    if pos >= 0:
                        res.append({'room': name, 'x': pos, 'step': sideroom['step'] + pos + 1})

        return res


energy = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


def possible_moves(onestate, prof):
    players = onestate['players']
    cost = onestate['cost']
    # histo = onestate['histo']

    map = Labyrinth(prof)
    map.place(*players)

    states = []
    for ip, p in enumerate(players):
        if p['name'] == p['room']:
            ok = True
            for i in range(p['x'], prof):
                if map.get(p['name'], i) != p['room']:
                    ok = False
                    break
            if ok:
                continue

        res = map.explore(p['name'], p['room'], p['x'])

        finish = [e for e in res if e['room'] == p['name']]
        if len(finish) > 0:
            res = [finish[0]]

        for newpos in res:
            playerscopy = [e.copy() for e in players]
            playerscopy[ip].update(room=newpos['room'], x=newpos['x'])
            # newhisto = histo.copy()
            # newhisto.append((p['name'], newpos['room'], newpos['x']))
            # states.append({'players': playerscopy, 'cost': cost + energy[p['name']] * newpos['step'], 'histo': newhisto})
            total = cost + energy[p['name']] * newpos['step']
            guess = total + estimate_cost(playerscopy, map, prof)
            states.append({'players': playerscopy, 'cost': total, 'guess': guess})
    return states


def good_position(players):
    bad = 0
    for p in players:
        if p['name'] != p['room']:
            bad += 1

    return bad == 0


def estimate_cost(players, m, prof):
    cost = 0
    for p in players:
        step = 0
        if p['room'] == p['name']:
            for i in range(p['x'] + 1, prof):
                if m.get(p['name'], i) != p['room']:
                    step = p['x'] + 4
                    break

        else:
            indice_cible = Labyrinth.siderooms[p['name']]
            if p['room'] not in 'ABCD':
                step = abs(p['x'] - indice_cible) + 1
            else:
                step = p['x'] + abs(Labyrinth.siderooms[p['room']] - indice_cible) + 2

        cost += step * energy[p['name']]
    return cost


def load_input(filename):
    players = []
    with open(filename, 'r') as f:
        for ix, line in enumerate(f):
            for iy, cell in enumerate(line):
                if cell in 'ABCD':
                    if ix == '1':
                        room = 'H'
                        x = iy - 1
                    else:
                        room = Labyrinth.siderooms[iy-1]
                        x = ix - 2
                    players.append({'name': cell, 'room': room, 'x': x})
    return players


def test1():
    map = Labyrinth()

    map.display()
    print('* explore')
    res = map.explore('A', 'B', 0)
    for e in res:
        print(e)
    print('* explore')
    res = map.explore('D', 'B', 1)
    for e in res:
        print(e)

    print('* explore')
    res = map.explore('D', 'H', 1)
    for e in res:
        print(e)


def test2():
    map = Labyrinth(4)

    p1 = {'name': 'B', 'room': 'C', 'x': 1}
    p2 = {'name': 'A', 'room': 'A', 'x': 0}
    p3 = {'name': 'B', 'room': 'B', 'x': 1}

    map.place(p1, p2, p3)

    map.display()
    print('* explore')
    res = map.explore('B', 'H', 0)
    for e in res:
        print(e)
    print('* explore')
    res = map.explore('D', 'A', 1)
    for e in res:
        print(e)


def partX(players, prof):
    tocheck = [{'players': players, 'guess': 0, 'cost': 0, 'histo': []}]
    minfinish = None
    while len(tocheck) > 0:
        # tocheck.sort(key=lambda x: x['guess'], reverse=True)

        state = tocheck.pop()
        newstates = []
        for e in possible_moves(state, prof):
            if good_position(e['players']):
                if minfinish is None or e['cost'] < minfinish['cost']:
                    print('FIND', e['cost'])  #, e['histo'])
                    minfinish = e
            else:
                if minfinish is None or e['guess'] < minfinish['cost']:
                    newstates.append(e)

        tocheck.extend(newstates)

    print('FINISH', minfinish)


def part1():
    players = load_input('input')
    m = Labyrinth(2)
    m.place(*players)
    m.display()

    print(players)
    partX(players, 2)


def part2():
    players = load_input('input')

    for p in players:
        if p['x'] == 1:
            p['x'] += 2
    players.extend([
        {'name': 'D', 'room': 'A', 'x': 1},
        {'name': 'D', 'room': 'A', 'x': 2},
        {'name': 'C', 'room': 'B', 'x': 1},
        {'name': 'B', 'room': 'B', 'x': 2},
        {'name': 'B', 'room': 'C', 'x': 1},
        {'name': 'A', 'room': 'C', 'x': 2},
        {'name': 'A', 'room': 'D', 'x': 1},
        {'name': 'C', 'room': 'D', 'x': 2},
    ])

    m = Labyrinth(4)
    m.place(*players)

    m.display()
    partX(players, 4)


if __name__ == '__main__':
    part1()
    part2()