import pycommon as M
from collections import deque, Counter, defaultdict
import math


class Module:
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs

    def _make_outputs(self, pulse, outputs):
        return [(self.name, pulse, o) for o in outputs]

    def _receive(self, origin, pulse):
        return pulse, self.outputs

    def receive(self, origin, pulse):
        opulse, outputs = self._receive(origin, pulse)
        return self._make_outputs(opulse, outputs)


class Broadcaster(Module):
    pass


class Flipflop(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.ison = False

    def _receive(self, origin, pulse):
        opulse = 0
        if pulse == 1:
            outputs = []
        else:
            outputs = self.outputs
            if not self.ison:
                opulse = 1
            self.ison = not self.ison
        return opulse, outputs


class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.memory = {}

    def set_links(self, names):
        self.memory = {n: 0 for n in names}

    def _receive(self, origin, pulse):
        self.memory[origin] = pulse
        M.debug('mem %s %s', list(self.memory.items()), all([e == 1 for e in self.memory.values()]))

        opulse = 0 if all([e == 1 for e in self.memory.values()]) else 1
        return opulse, self.outputs


def load_input(filename):
    circuit = {}
    conjonction = {}
    with open(filename, 'r') as f:
        for line in f:
            items = line.split()
            outputs = [o.strip(', ') for o in items[2:]]
            if items[0][0] == '&':
                circuit[items[0][1:]] = Conjunction(items[0][1:], outputs)
                conjonction[items[0][1:]] = []
            elif items[0][0] == '%':
                circuit[items[0][1:]] = Flipflop(items[0][1:], outputs)
            else:
                circuit[items[0]] = Broadcaster(items[0][1:], outputs)

    for name, link in conjonction.items():
        for nc, c in circuit.items():
            for o in c.outputs:
                if o == name:
                    link.append(nc)
        M.debug('Conjonction %s with links %s', name, link)
        circuit[name].set_links(link)

    return circuit


def push_button(circuit, watch=()):
    pulses = deque([('button', 0, 'broadcaster')])
    M.debug("* PUSH *")
    count = Counter()
    while pulses:
        p = pulses.popleft()
        M.debug("process %s", p)
        if p[0] in watch and p[1] == 1:
            count[p[0]] += 1
            M.debug(' - watched pulse: %s', count[p[0]])
        count[p[1]] += 1
        if p[2] in circuit:
            opulses = circuit[p[2]].receive(p[0], p[1])
            pulses.extend(opulses)

    return count


@M.timeperf
def test():
    M.log()
    circuit = load_input('input_test')
    print(circuit)
    cl, ch = 0, 0
    for i in range(2):
        c = push_button(circuit)
        cl += c[0]
        ch += c[1]
    print(cl, ch)

    M.nolog()
    circuit = load_input('input')
    # rx comes after vd, which is a conjonction with inputs : ['rd', 'bt', 'fv', 'pr']
    for name, c in circuit.items():
        if 'rx' in c.outputs:
            before_rx = name
    print('before rx', before_rx)

    for name, c in circuit.items():
        if name == before_rx:
            assert isinstance(c, Conjunction), 'Hoho pas le meme type de circuit que dans mon input'
            ref = list(c.memory.keys())

    print('link with', before_rx, ':', ref)


@M.timeperf
def part1():
    M.nolog()
    circuit = load_input('input')
    cl, ch = 0, 0
    for i in range(1000):
        c = push_button(circuit)
        cl += c[0]
        ch += c[1]
    print('part1', cl * ch)


@M.timeperf
def part2():
    circuit = load_input('input')
    for name, c in circuit.items():
        if 'rx' in c.outputs:
            before_rx = name

    for name, c in circuit.items():
        if name == before_rx:
            assert isinstance(c, Conjunction), 'Hoho pas le meme type de circuit'
            ref = list(c.memory.keys())

    cycles = defaultdict(list)

    indice = 0
    while True:
        indice += 1
        c = push_button(circuit, watch=ref)

        for n in ref:
            if n in c:
                cycles[n].append(indice)
                print(n, indice)

        if len(cycles) == 4 and all(len(v) >= 2 for v in cycles.values()):
            for v in cycles.values():
                assert v[0] == v[1] - v[0], 'GOTO reste chinois...'
            print('part2', math.lcm(*list([v[0] for v in cycles.values()])))
            break


if __name__ == '__main__':
    test()
    part1()
    part2()
