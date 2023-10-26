def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            pattern, digits = line.rstrip().split('|')
            pattern = pattern.strip().split()
            digits = digits.strip().split()
            res.append((pattern, digits))

    return res


def easy_mapping(seg):
    n = len(seg)
    res = None
    if n == 2:
        res = 1
    elif n == 3:
        res = 7
    elif n == 4:
        res = 4
    elif n == 7:
        res = 8

    return res


def compile(pattern):
    mapping = {}
    hard_pattern = []
    for p in pattern:
        n = easy_mapping(p)
        if n is not None:
            mapping[n] = set(p)
        else:
            hard_pattern.append(set(p))

    top = mapping[7] - mapping[1]
    mapping[9] = [p for p in hard_pattern if mapping[4] | top <= p][0]
    bottonleft = mapping[8] - mapping[9]

    for p in hard_pattern:
        if len(p) == 5 and bottonleft <= p:
            mapping[2] = p
        elif len(p) == 5 and mapping[1] <= p:
            mapping[3] = p
        elif len(p) == 6 and not mapping[1] <= p:
            mapping[6] = p

    mapping[5] = mapping[6] - bottonleft
    mapping[0] = [p for p in hard_pattern if p not in mapping.values()][0]

    print(mapping)

    rev_mapping = dict((tuple(sorted(list(v))), k) for k, v in mapping.items())

    return rev_mapping


def to_num(li):
    res = 0
    for d in li:
        res = 10 * res + d
    return res


if __name__ == '__main__':
    data = load_input('input')

    count = 0
    total = 0
    for t in data:
        easy = [e for e in t[1] if easy_mapping(e) is not None]
        count += len(easy)

        m = compile(t[0])

        digits = [m[tuple(sorted(list(p)))] for p in t[1]]
        n = to_num(digits)
        total += n
        print(n)


    print(count)
    print(total)