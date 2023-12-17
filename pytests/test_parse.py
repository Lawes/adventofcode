import unittest
import os
import pycommon as M


class TestParse(unittest.TestCase):
    def test_ints_txt(self):
        self.assertEqual(M.ints_txt(''), [])

        self.assertEqual(M.ints_txt('dcsc sdf dfg df '), [])

        self.assertEqual(M.ints_txt('dcsc sdf 1dfg df -'), [1])

        self.assertEqual(
            M.ints_txt('1 2 dfdfdf3 ojjmo-5\nsdfdfsdc678-2\n'),
            [1, 2, 3, -5, 678, -2])

    def test_ints_file(self):
        testfile = os.path.join(os.path.dirname(__file__), 'input_ints_file.txt')

        self.assertEqual(
            M.ints_file(testfile),
            [[], [], [1, 2, 3, -5], [678, -2]])

    def test_grid_txt(self):
        self.assertEqual(M.grid_txt('', {}), ({}, 0, 0))

        self.assertEqual(M.grid_txt('4545', {}), ({}, 4, 1))

        self.assertEqual(
            M.grid_txt('4545', {'5': '#'}),
            ({(1, 0): '#', (3, 0): '#'}, 4, 1))

        self.assertEqual(
            M.grid_txt('4545\n50', {'5': '#'}),
            ({(1, 0): '#', (3, 0): '#', (0, 1): '#'}, 4, 2))


if __name__ == '__main__':
    unittest.main()
