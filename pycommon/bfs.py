from .mylog import is_log_enable, debug
from collections import deque


class AocBfs:
    """
    IMPL
    def get_voisins(self, state):
    def is_end(self, state):
    def make_key(self, state):
    """
    def __init__(self):
        self.stop_after = None

    def set_stop_after(self, i):
        self.stop_after = i

    def get_voisins(self, state):
        raise NotImplementedError()

    def is_end(self, state):
        raise NotImplementedError()

    def make_key(self, state):
        raise NotImplementedError()

    def search(self, *states0):
        count_deque = 0
        step = 0

        queue = deque([(step, s) for s in states0])
        cache = set()

        while queue:
            imove, state = queue.popleft()
            debug('BFS pickup %s, %s', imove, state)
            choices = self.get_voisins(state)
            if is_log_enable:
                debug('BFS get_voisins:')
                for s in choices:
                    debug('    - %s', s)

            count_deque += 1
            imove += 1

            for s in choices:
                if self.is_end(s):
                    return imove, s
                key = self.make_key(s)
                debug('BFS make_key %s <- %s', key, s)
                if key in cache:
                    debug('BFS key in cache')
                    continue
                queue.append((imove, s))
                cache.add(key)
            if self.stop_after is not None and self.stop_after == count_deque:
                break
            debug('BFS #queue %s', len(queue))
        return -1
