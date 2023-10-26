import numpy as np

def load_input(filename):
    operations = []
    with open(filename, 'r') as f:
        for line in f:
            offset = 0
            if line.startswith('turn on'):
                action = 1
                offset = 1
            elif line.startswith('turn off'):
                action = -1
                offset = 1
            else:
                action = 0

            tokens = line.split()

            testc1 = [int(v) for v in tokens[1 + offset].split(',')]
            testc2 = [int(v) for v in tokens[3 + offset].split(',')]

            c1 = (min(testc1[0], testc2[0]), min(testc1[1], testc2[1]))
            c2 = (max(testc1[0], testc2[0])+1, max(testc1[1], testc2[1])+1)

            operations.append({'action': action, 'c1': c1, 'c2': c2})
    return operations


def do_turnon(grid, c1, c2):
    grid[c1[0]:c2[0], c1[1]:c2[1]] = 1


def do_turnoff(grid, c1, c2):
    grid[c1[0]:c2[0], c1[1]:c2[1]] = 0


def do_toggle(grid, c1, c2):
    grid[c1[0]:c2[0], c1[1]:c2[1]] = np.remainder(grid[c1[0]:c2[0], c1[1]:c2[1]] + 1, 2)


def do_turnon2(grid, c1, c2):
    grid[c1[0]:c2[0], c1[1]:c2[1]] += 1


def do_turnoff2(grid, c1, c2):
    grid[c1[0]:c2[0], c1[1]:c2[1]] -= 1
    grid[grid < 0] = 0


def do_toggle2(grid, c1, c2):
    grid[c1[0]:c2[0], c1[1]:c2[1]] += 2


if __name__ == '__main__':
    operations = load_input('input')

    grid = np.zeros((1000, 1000))
    for op in operations:
        if op['action'] == 1:
            func = do_turnon
        elif op['action'] == -1:
            func = do_turnoff
        else:
            func = do_toggle

        func(grid, op['c1'], op['c2'])

    print('part1', np.sum(grid == 1))

    grid = np.zeros((1000, 1000))
    for op in operations:
        if op['action'] == 1:
            func = do_turnon2
        elif op['action'] == -1:
            func = do_turnoff2
        else:
            func = do_toggle2

        func(grid, op['c1'], op['c2'])

    print('part2', np.sum(grid))