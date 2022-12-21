from scipy import optimize


def load_input(filename):
    monkeys = {}
    with open(filename, 'r') as f:
        for line in f:
            name, job = [e.strip() for e in line.split(':')]

            try:
                val = int(job)
                monkeys[name] = val
                continue
            except Exception:
                pass

            monkeys[name] = job.split()
    return monkeys


def monkey_yell(name, monkeys, cache):
    if name in cache:
        return cache[name]

    if isinstance(t := monkeys[name], int):
        res = t
    else:
        v1 = monkey_yell(t[0], monkeys, cache)
        v2 = monkey_yell(t[2], monkeys, cache)
        if t[1] == '+':
            res = v1 + v2
        elif t[1] == '-':
            res = v1 - v2
        elif t[1] == '*':
            res = v1 * v2
        elif t[1] == '/':
            res = v1 // v2

    cache[name] = res
    return res


def test():
    monkeys = load_input('input_test')

    print(monkey_yell('root', monkeys, {}))

    rootcheck = monkeys.pop('root')

    monkeys['humn'] = 0

    cache = {}

    print(monkey_yell(rootcheck[0], monkeys, cache))
    print(monkey_yell(rootcheck[2], monkeys, cache))


def part1():
    monkeys = load_input('input')
    print('part1', monkey_yell('root', monkeys, {}))


def part2():
    monkeys = load_input('input')
    rootcheck = monkeys.pop('root')

    def f(humn):
        cache = {}
        monkeys['humn'] = int(humn)
        return monkey_yell(rootcheck[0], monkeys, cache) - monkey_yell(rootcheck[2], monkeys, cache)

    print('part2', int(optimize.newton(f, 100000, tol=1)))


if __name__ == '__main__':
    part2()
