from .mylog import is_log_enable, debug
from collections import deque


class AocBfs:
    """
    IMPL
    def get_voisins(self, state):
    def is_end(self, state):
    def make_key(self, state):
    """
    stop_after = None

    def set_stop_after(self, i):
        self.stop_after = i

    def get_voisins(self, state):
        raise NotImplementedError('get_voisins')

    def is_end(self, state):
        raise NotImplementedError('is_end')

    def make_key(self, state):
        return state

    def next(self):
        while self.lopen:
            imove, state = self.lopen.popleft()
            debug('')
            debug('BFS #queue %s, pickup %s %s', len(self.lopen), imove, state)
            if self.is_end(state):
                return imove, state

            choices = self.get_voisins(state)
            if is_log_enable:
                debug('BFS get_voisins:')
                for s, c in choices:
                    debug('    - %s', s)

            self.count_deque += 1

            for s, c in choices:
                smoves = imove + c
                key = self.make_key(s)
                debug('BFS make_key %s <- %s', key, s)
                if key in self.cache:
                    debug('BFS key in cache')
                    continue
                self.lopen.append((smoves, s))
                self.cache.add(key)
            if self.stop_after is not None and self.stop_after == self.count_deque:
                break
        return None

    def search(self, *states0):
        self.count_deque = 0
        self.lopen = deque([(0, s) for s in states0])
        self.cache = set([self.make_key(s) for s in states0])

        return self.next()
