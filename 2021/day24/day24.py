import random
import itertools
import numpy as np
from collections import defaultdict
import json
import os

_refnum, _comp_func = '', max
_refnum, _comp_func = '999999999999999999999999999', min


def gen_random():
    while True:
        yield random.randint(1, 9)


def gen_one(num):
    while True:
        yield num


class ALU:
    def __init__(self):
        self.reset()

    def reset(self):
        self.memory = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.memory[k] = v

    def input(self, it):
        self.inputs = iter(it)

    def getValue(self, x):
        if isinstance(x, int):
            return x
        return self.memory[x]

    def inp(self, lh):
        self.memory[lh] = next(self.inputs)

    def add(self, lh, rh):
        self.memory[lh] += self.getValue(rh)

    def mul(self, lh, rh):
        self.memory[lh] *= self.getValue(rh)

    def div(self, lh, rh):
        self.memory[lh] //= self.getValue(rh)

    def mod(self, lh, rh):
        self.memory[lh] %= self.getValue(rh)

    def eql(self, lh, rh):
        self.memory[lh] = 1 if self.getValue(rh) == self.memory[lh] else 0

    def play(self, *args):
        mapping = {
            'add': self.add,
            'mul': self.mul,
            'div': self.div,
            'mod': self.mod,
            'eql': self.eql,
            'inp': self.inp
        }
        # print('-', args)
        mapping[args[0]](*args[1:])
        # self.displayMemory()

    def displayMemory(self):
        print(' - '.join(['{0}:{1}'.format(k, v) for k, v in self.memory.items()]))

    def isValid(self):
        return self.memory['z'] == 0



class ALUvector:
    def __init__(self, s):
        self.size = s
        self.reset()

    def zeros(self):
        return np.zeros(self.size, dtype=int)

    def reset(self):
        self.memory = {
            'w': self.zeros(),
            'x': self.zeros(),
            'y': self.zeros(),
            'z': self.zeros()
        }

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.memory[k] = v

    def input(self, it):
        self.inputs = iter(it)

    def getValue(self, x):
        if isinstance(x, int):
            return x
        return self.memory[x]

    def inp(self, lh):
        self.memory[lh] = self.zeros() + next(self.inputs)

    def add(self, lh, rh):
        self.memory[lh] += self.getValue(rh)

    def mul(self, lh, rh):
        self.memory[lh] *= self.getValue(rh)

    def div(self, lh, rh):
        self.memory[lh] //= self.getValue(rh)

    def mod(self, lh, rh):
        self.memory[lh] %= self.getValue(rh)

    def eql(self, lh, rh):
        try:
            self.memory[lh] = (self.memory[lh] == self.getValue(rh)).astype(int)
        except Exception:
            print(type(self.memory[lh]), type(self.getValue(rh)), self.memory[lh] == self.getValue(rh))

    def play(self, *args):
        mapping = {
            'add': self.add,
            'mul': self.mul,
            'div': self.div,
            'mod': self.mod,
            'eql': self.eql,
            'inp': self.inp
        }
        # print('-', args)
        mapping[args[0]](*args[1:])
        # self.displayMemory()

    def displayMemory(self):
        print(' - '.join(['{0}:{1}'.format(k, v) for k, v in self.memory.items()]))

    def findValid(self, z=0):
        return self.memory['z'] == z



def split_op(instructions):
    bulks = []

    current = []
    for op in instructions:
        if op[0] == 'inp':
            if len(current) > 0:
                bulks.append(current)
            current = []
        current.append(op)

    bulks.append(current)
    return bulks


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) > 2:
                try:
                    rh = int(tokens[2])
                except Exception:
                    rh = tokens[2]
                res.append((tokens[0], tokens[1], rh))
            else:
                res.append((tokens[0], tokens[1]))
    return res


def test1():
    instructions = load_input('input')

    alu = ALU()
    # alu.input(gen_random())
    alu.input([9] * 14)

    for op in instructions:
        alu.play(*op)

    print(alu.isValid())


def explore_depth(list_bulk):
    alu = ALU()

    tocheck = {0: ''}
    for depth, bulk in enumerate(list_bulk):
        newcheck = {}
        for zprevious, num in tocheck.items():
            for inp in range(1, 10):
                alu.set(z=zprevious)
                alu.input([inp])
                for op in bulk:
                    alu.play(*op)
                nextnum = num + str(inp)
                z = alu.memory['z']
                # newcheck[z] = max(newcheck.get(z, ''), nextnum)
                newcheck[z] = _comp_func(newcheck.get(z, _refnum), nextnum)
        print('*', depth, len(newcheck))
        tocheck = newcheck
    return tocheck


def checkValid(instructions, n, z0, zgoals):
    alu = ALU()
    # for seq in itertools.product(range(9, -1, -1), repeat=n):
    for seq in itertools.product(range(1, 10), repeat=n):
        alu.reset()
        alu.set(z=z0)
        alu.input(seq)
        for op in instructions:
            alu.play(*op)
        # print('check', seq, alu.memory['z'])
        if alu.memory['z'] in zgoals:
            return ''.join([str(e) for e in seq]) + zgoals[alu.memory['z']]


def explore_inverse(list_bulk):
    Z = np.arange(0, 500000, dtype=int)

    alu = ALUvector(len(Z))

    previous = {0: ''}
    for depth, sub in enumerate(list_bulk[::-1]):
        newres = {}
        for goal, num in previous.items():

            for inp in range(1, 10):
                alu.set(z=Z.copy())
                alu.input([inp])
                for op in sub:
                    alu.play(*op)
                indice = alu.findValid(goal)
                for zgoal in Z[indice]:
                    newres[int(zgoal)] = _comp_func(newres.get(zgoal, _refnum), str(inp) + num)
        print('*', depth, len(newres))
        previous = newres

    return previous




def test2():
    instructions = load_input('input')
    instructions_split = split_op(instructions)
    len(instructions_split)

    prof = 8
    tocheck = explore_depth(instructions_split[:prof])

    minz = min(tocheck.keys())
    maxz = max(tocheck.keys())
    print(minz, maxz, len(tocheck))
    return


def test3():
    instructions = load_input('input')
    instructions_split = split_op(instructions)
    len(instructions_split)

    ezinv = explore_inverse(instructions_split[12:])
    print(ezinv)

    # sub_instructions = itertools.chain(*instructions_split[13:])
    sub_instructions = []
    for bulk in instructions_split[12:]:
        sub_instructions.extend(bulk)

    for zgoal in ezinv:
        print(checkValid(sub_instructions, 2, zgoal))


def test0():
    instructions = load_input('input')
    count = 0

    for seq in itertools.product([9, 8, 7, 6, 5, 4, 3, 2, 1], repeat=14):
        count += 1
        if count % 10000000 == 0:
            print('*', seq)
        alu = ALU()
        alu.input(seq)
        for op in instructions:
            alu.play(*op)
        if alu.isValid():
            print('FIND', seq)


def part1():
    instructions = load_input('input')
    instructions_split = split_op(instructions)
    len(instructions_split)

    prof = 9
    filename = 'zdepth.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            zdepth = json.load(f)
    else:
        zdepth = explore_depth(instructions_split[:prof])
        zdepth = sorted(zdepth.items(), key=lambda x: x[1], reverse=True)
        print('* write zdepth.json')
        with open('zdepth.json', 'w') as f:
            json.dump(zdepth, f)

    iprof = 10
    filename = 'zinv.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            zinv = dict(json.load(f))
    else:
        zinv = explore_inverse(instructions_split[iprof:])
        print('* write zinv.json')
        with open(filename, 'w') as f:
            json.dump(list(zinv.items()), f)

    sub_instructions = []
    for bulk in instructions_split[prof:iprof]:
        sub_instructions.extend(bulk)

    max_part1 = None
    max_part2 = ''
    for zinit, num in zdepth:
        v = checkValid(sub_instructions, iprof - prof, zinit, zinv)
        # v = None
        # if zinit in zinv:
        #    v = zinv[zinit]

        if v is not None:
            if max_part1 is not None and num < max_part1:
                break
            if max_part1 is None:
                max_part1 = num
                max_part2 = v
                print(max_part1, max_part2)
            else:
                max_part2 = max(max_part2, v)
                print(max_part1, max_part2)

    print('MAX', max_part1, max_part2)

def part2():
    instructions = load_input('input')
    instructions_split = split_op(instructions)
    len(instructions_split)

    prof = 9
    filename = 'zdepth2.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            zdepth = json.load(f)
    else:
        zdepth = explore_depth(instructions_split[:prof])
        zdepth = sorted(zdepth.items(), key=lambda x: x[1])
        print('* write zdepth2.json')
        with open(filename, 'w') as f:
            json.dump(zdepth, f)

    iprof = 10
    filename = 'zinv2.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            zinv = dict(json.load(f))
    else:
        zinv = explore_inverse(instructions_split[iprof:])
        print('* write zinv2.json')
        with open(filename, 'w') as f:
            json.dump(list(zinv.items()), f)

    sub_instructions = []
    for bulk in instructions_split[prof:iprof]:
        sub_instructions.extend(bulk)

    min_part1 = None
    min_part2 = _refnum
    for zinit, num in zdepth:
        v = checkValid(sub_instructions, iprof - prof, zinit, zinv)
        # v = None
        # if zinit in zinv:
        #    v = zinv[zinit]

        if v is not None:
            if min_part1 is not None and num > min_part1:
                break
            if min_part1 is None:
                min_part1 = num
                min_part2 = v
                print(min_part1, min_part2)
            else:
                min_part2 = _comp_func(min_part2, v)
                print(min_part1, min_part2)

    print('MIN', min_part1, min_part2)


if __name__ == '__main__':
    part2()


