import unittest
import pycommon as M


class TestBfs(unittest.TestCase):
    def setUp(self):
        self. graph = {
            'A': ['B', 'C', 'D'],
            'B': [],
            'C': ['E', 'F'],
            'D': ['G'],
            'E': [],
            'F': ['D'],
            'G': ['H'],
            'H': ['B']
        }

    def test_init(self):
        try:
            class Bfs(M.AocBfs):
                def get_voisins(self, state):
                    return []
        except Exception:
            self.fail('Bfs impossible to create')

    def test_search(self):
        class Bfs(M.AocBfs):
            def __init__(self, graph):
                self.graph = graph

            def get_voisins(self, state):
                return [(n, 1) for n in self.graph.get(state, [])]

            def is_end(self, state):
                return state == 'H'

        algo = Bfs(self.graph)
        self.assertEqual(algo.search('A'), (3, 'H'))
        self.assertEqual(algo.search('C'), (4, 'H'))

    def test_next(self):
        class Bfs(M.AocBfs):
            def __init__(self, graph):
                self.graph = graph

            def get_voisins(self, state):
                return [(n, 1) for n in self.graph.get(state, [])]

            def is_end(self, state):
                return state in 'DF'

        algo = Bfs(self.graph)
        self.assertEqual(algo.search('A'), (1, 'D'))
        self.assertEqual(algo.next(), (2, 'F'))


if __name__ == '__main__':
    unittest.main()
