
def load_input(filename):
    with open(filename, 'r') as f:
        res = [line.strip() for line in f]

    return res


def priority(c):
    c0 = 96 if 'a' <= c <= 'z' else 38
    return ord(c) - c0


def part1(sacados):
    total = 0
    for sac in sacados:
        n = len(sac)//2
        p1 = sac[:n]
        p2 = sac[n:]
        total += priority(set(p1).intersection(p2).pop())
    return total


def part2(sacados):
    return sum(
        priority(
            set(sacados[i]).intersection(sacados[i+1]).intersection(sacados[i+2]).pop())
        for i in range(0, len(sacados), 3)
    )


if __name__ == '__main__':

    for c in 'azAZ':
        print(priority(c))

    sacados = load_input('input_test')
    print('test', part1(sacados))
    print('test', part2(sacados))

    sacados = load_input('input')
    print('#sac', len(sacados), ',badges', len(sacados)/3)
    print('part1', part1(sacados))
    print('part2', part2(sacados))
