from itertools import combinations
import re
import sys

_pattern = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)')


def dijkstra(k0, G):
    m = len(G) + 1

    C = {k: m for k in G}

    lclose = set()
    lopen = set([k0])

    C[k0] = 0

    while len(lopen) > 0:
        k = min(lopen, key=lambda x: C[x])
        lopen.remove(k)

        cost_path = C[k]
        lclose.add(k)

        for kk in G[k][1]:
            if kk in lclose:
                continue

            ncost = cost_path + 1
            if ncost < C[kk]:
                C[kk] = ncost

            if kk not in lclose:
                lopen.add(kk)

    return C


class GraphState:
    def __init__(self):
        self.g = {}
        self.c = {}
        self.maxrate = 0
        self.clear_state()

    def clear_state(self):
        self.actions = []
        self.set_blacklist(set())

    def add(self, name, rate, edges):
        self.g[name] = (rate, edges)
        self.maxrate = sum([e[0] for e in self.g.values()])

    def set_begin(self, node):
        self.start = node

    def dijkstra(self):
        for k in self.g:
            self.c[k] = dijkstra(k, self.g)

    def choices(self):
        return [k for k in self.g if self.needToOpen(k)]

    def isAllOpen(self):
        return len(self.choices()) == 0

    def set_blacklist(self, bl):
        self.blacklist = bl

    def needToOpen(self, node):
        return node not in self.blacklist and node not in self.actions and self.g[node][0] != 0

    def do_action(self, a):
        self.actions.append(a)

    def undo(self):
        self.actions.pop()

    def path_time(self):
        current = self.start
        total = 0
        for a in self.actions:
            total += self.c[current][a] + 1
            current = a
        return total

    def total_flow(self, maxtime):
        current = self.start
        currentTime = maxtime
        total = 0
        for a in self.actions:
            currentTime -= self.c[current][a] + 1
            total += currentTime * self.g[a][0]
            current = a

        return total


def load_input(filename):
    G = GraphState()
    with open(filename, 'r') as f:
        for line in f:
            # print(repr(line))
            m = _pattern.match(line)
            name = m.group(1)
            G.add(name, int(m.group(2)), [e for e in m.group(3).replace(',', '').split()])
    return G


def explore(graph, depth):

    if graph.isAllOpen():
        return (graph.total_flow(depth), graph.actions[:])

    current_flow = graph.total_flow(depth)
    current_actions = graph.actions[:]

    tries = []
    for node in graph.choices():
        graph.do_action(node)
        if graph.path_time() > depth:
            tries.append((current_flow, current_actions))
        else:
            tries.append(explore(graph, depth))
        graph.undo()

    return max(tries)


def test():
    G = load_input('input_test')
    print(G.g)

    for k, v in G.g.items():
        print(k, v[1])

    # print(G.g.keys())

    G.dijkstra()

    # print(G.c)

    G.set_begin('AA')

    for a in ['BB']:
        G.do_action(a)
    print(G.total_flow(30))

    G.clear_state()
    print(explore(G, 30))


def part1():
    G = load_input('input')
    # for k, v in G.g.items():
    #     print(k, v[1])

    G.dijkstra()
    print('coucou')

    G.set_begin('AA')

    print(G.choices())

    print('part1', explore(G, 30))


def part2():
    G1 = load_input('input')
    G1.dijkstra()
    G1.set_begin('AA')

    G2 = load_input('input')
    G2.c = G1.c
    G2.set_begin('AA')

    allchoices = set(G1.choices())
    previous = []

    maxflow = 0
    for n in range(1, len(allchoices)//2 + 1):
        print('*', n, '/', len(allchoices)//2 + 1)
        for p in combinations(allchoices, n):
            sp = set(p)
            comp = allchoices - sp

            G1.set_blacklist(comp)
            G2.set_blacklist(sp)

            e1 = None
            for res in previous:
                if sp.issubset(res['in']) and res['out'].issubset(sp):
                    e1 = res['val']
                    break

            e2 = None
            for res in previous:
                if comp.issubset(res['in']) and res['out'].issubset(comp):
                    e2 = res['val']
                    break

            if e1 is None:
                e1 = explore(G1, 26)
                previous.append({'in': sp, 'out': set(e1[1]), 'val': e1[0]})
                e1 = e1[0]

            if e2 is None:
                e2 = explore(G2, 26)
                previous.append({'in': comp, 'out': set(e2[1]), 'val': e2[0]})
                e2 = e2[0]

            v = e1 + e2

            if v > maxflow:
                maxflow = v
                print(maxflow)


if __name__ == '__main__':
    part2()
