from .mylog import debug
import heapq


class AocDijkstra:
    """
    IMPL
    def get_voisins(self, state):
    def is_end(self, state):
    """

    def get_voisins(self, state):
        """
        return [(state, delta_cost), ...]
        """
        raise NotImplementedError('get_voisins')

    def is_end(self, state):
        return False

    def make_key(self, state):
        return state

    def search(self, state0, cost0=0, maxcost=10**20):
        self.lclose = set()
        self.lopen = [(cost0, state0)]
        self.cost = {self.make_key(state0): (cost0, None)}

        self.maxcost = maxcost

        return self.next()

    def next(self):
        emptystate = (self.maxcost, None)
        while self.lopen:
            debug('')
            cost, newstate = heapq.heappop(self.lopen)

            knewstate = self.make_key(newstate)
            debug('DIJKSTRA #open %s, pickup %s, cost %s', len(self.lopen), newstate, cost)

            if knewstate in self.lclose:
                debug('alreaydy in close')
                continue

            if self.is_end(newstate):
                debug('DIJKSTRA end')
                return cost, newstate

            self.lclose.add(knewstate)

            choices = self.get_voisins(newstate)
            debug('DIJKSTRA get_voisins:')
            for s, c in choices:
                debug('    - %s, corst %s', s, c)
                ks = self.make_key(s)
                if ks in self.lclose:
                    continue

                newcost = cost + c
                if newcost < self.cost.get(ks, emptystate)[0]:
                    self.cost[ks] = (newcost, newstate)

                debug('DIJKSTRA add open %s', s)
                heapq.heappush(self.lopen, (self.cost[ks][0], s))
        return None

    def get_cost(self, state):
        ks = self.make_key(state)
        return self.cost[ks]

    def find_path(self, state):
        prev = state
        path = []
        while True:
            path.append(prev)
            prev = self.cost[self.make_key(prev)][1]
            if prev is None:
                break
        return path
