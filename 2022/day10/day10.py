
def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('noop'):
                res.append(None)
            elif line.startswith('addx'):
                res.append(int(line.split()[1]))
    return res


def signal_strengh(signal, nth):
    return signal[nth-1] * nth


def play_instruction(inst, val):
    if inst is None:
        return [val], val
    return [val, val], val+inst


if __name__ == '__main__':
    instructions = load_input('input')

    signal = []
    register = 1

    for inst in instructions:
        t, register = play_instruction(inst, register)
        signal += t

    print('part1', sum(signal_strengh(signal, n) for n in range(20, 240, 40)))

    CRT = []
    current = ''
    for ipos, pos in enumerate(signal):
        relpos = pos % 40
        if ipos % 40 == 0:
            CRT.append(current)
            current = ''
        drawpos = len(current)

        if relpos-1 <= drawpos <= relpos+1:
            current += '#'
        else:
            current += '.'

    CRT.append(current)

    print('\n'.join(CRT))
