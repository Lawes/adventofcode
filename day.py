import pycommon as M


def load_input(filename):
    with open(filename, 'r') as f:
        pass


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')


@M.timeperf
def part1():
    data = load_input('input')

    print('part1')


@M.timeperf
def part2():
    data = load_input('input')

    print('part2')


if __name__ == '__main__':
    test()