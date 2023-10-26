from collections import Counter, defaultdict

def load_input(filename):
    with open(filename, 'r') as f:
        template = next(f).strip()
        next(f)

        rules = {}
        for line in f:
            pair, _, insert = line.strip().split()
            rules[pair] = insert
    return template, rules


def step(sentence, rules):
    n = len(sentence)
    res = []
    for i in range(n-1):
        res.append(sentence[i])
        pair = sentence[i] + sentence[i+1]

        res.append(rules.get(pair, ''))
    
    res.append(sentence[-1])
    return ''.join(res)


def create_pairs(sentence):
    return Counter([''.join(p) for p in zip(sentence[:-1], sentence[1:])])


def step_pairs(cpairs, rules):
    newcount = defaultdict(int)
    for p, v in cpairs.items():
        if p in rules:
            c = rules[p]
            p1 = p[0] + c
            p2 = c + p[1]
            newcount[p1] += v
            newcount[p2] += v

    return newcount




if __name__ == '__main__':
    template, rules = load_input('input')

    print(template)
    print(rules)

    s = template

    for istep in range(10):
        s = step(s, rules)
        print(istep, Counter(s).most_common(1))

    c = Counter(s).most_common()
    print(c[0][1] - c[-1][1])

    cpairs = create_pairs(template)

    for istep in range(40):
        cpairs = step_pairs(cpairs, rules)

    res = defaultdict(int)
    for pair, v in cpairs.items():
        res[pair[0]] += v

    res[template[-1]] += 1

    print(res)

    cmax = max(res.items(), key=lambda x: x[1])
    cmin = min(res.items(), key=lambda x: x[1])

    print(cmax, cmin)

    print(cmax[1] - cmin[1])

    