
def load_input(filename):
    with open(filename, 'r') as f:
        firstline = next(f)

        n = len(firstline)
        ncols = int((n + 1)/4)
        stacks = [list() for _ in range(ncols)]
        current = firstline
        while not current.startswith(' 1'):
            for i in range(0, ncols):
                val = current[i*4 + 1]
                if val != ' ':
                    stacks[i].append(val)
            current = next(f)

        stacks = [u[::-1] for u in stacks]

        instructions = []
        for line in f:
            items = line.split()
            if len(items) > 5:
                instructions.append({'n': int(items[1]), 'from': int(items[3]), 'to': int(items[5])})

    return stacks, instructions


def apply_one(stacks, fr, to, n):
    s = len(stacks[fr-1])
    n2move = min(s, n)
    stacks[to-1].extend(stacks[fr-1][-n2move:])
    stacks[fr-1] = stacks[fr-1][:-n2move]


def apply_all_p1(stacks, instructions):
    for inst in instructions:
        for i in range(inst['n']):
            apply_one(stacks, inst['from'], inst['to'], 1)


def apply_all_p2(stacks, instructions):
    for inst in instructions:
        apply_one(stacks, inst['from'], inst['to'], inst['n'])


if __name__ == '__main__':
    stacks, instructions = load_input('input')

    print(stacks)
    apply_one(stacks, 1, 2, 3)
    print(stacks)

    apply_all_p1(stacks, instructions)
    print('part1', ''.join(u.pop() for u in stacks))

    stacks, instructions = load_input('input')
    apply_all_p2(stacks, instructions)
    print('part2', ''.join(u.pop() for u in stacks if u))
