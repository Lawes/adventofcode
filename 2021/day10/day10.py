import numpy as np

def load_input(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f]
    return lines


corresp_o = {
    ')': '(',
    '}': '{',
    ']': '[',
    '>': '<'
}

corresp_e = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

openchunk = set(corresp_e.keys())
endchunk = set(corresp_o.keys())


def check_line(line):
    state = dict((p, 0) for p in openchunk)

    stack = []

    for t in line:
        if t in openchunk:
            stack.append(t)
        elif t in endchunk:
            if corresp_o[t] == stack[-1]:
                stack.pop()
            else:
                return {'status': False, 'error': t}

    return {'status': True, 'seq': stack}


if __name__ == '__main__':
    score1 = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    score2 = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    lines = load_input('input')

    part1 = 0
    part2 = []
    for line in lines:
        res = check_line(line)

        if not res['status']:
            part1 += score1[res['error']]
        else:
            s = 0
            for i in [score2[corresp_e[t]] for t in res['seq'][::-1]]:
                s = s * 5 + i
            part2.append(s)

    print('part1', part1)
    print('part2', np.median(part2))


