import pycommon as M


def load_input(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


_conv = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

_inconv = '012=-'


def snafu2dec(txt):
    num = 0
    for v in txt:
        num = 5 * num + _conv[v]
    return num


def dec2snafu(num):
    txt = []
    M.debug('* %s', num)
    while num != 0:
        r = num % 5
        if r > 2:
            num += 5
        num //= 5
        M.debug('num:  %s, r: %s -> %s', num, r, _inconv[r])
        txt.append(_inconv[r])
    return ''.join(txt[::-1])


@M.timeperf
def test():
    M.log()
    print('2=-01', snafu2dec('2=-01'))
    for n in [0, 1, 2, 3, 4, 5]:
        print(str(n), dec2snafu(n))

    M.nolog()
    data = load_input('input_test')
    for sn in data:
        print(sn, snafu2dec(sn), dec2snafu(snafu2dec(sn)))


@M.timeperf
def part1():
    data = load_input('input')
    total = sum(snafu2dec(sn) for sn in data)

    print('part1', dec2snafu(total))


if __name__ == '__main__':
    part1()
