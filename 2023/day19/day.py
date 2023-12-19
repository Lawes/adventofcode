import pycommon as M
import re


pattern_cmp = re.compile(r'(\w+)([><])(\d+):(\w+)')


def parse_condition(txt):
    if (m:=pattern_cmp.match(txt)) is not None:
        func = (
            1 if m.group(2) == '<' else 2,
            m.group(1),
            int(m.group(3)),
            m.group(4)
        )
    else:
        func = (0, txt)
    return func


def load_input(filename):
    with open(filename, 'r') as f:
        content = f.read()
    block1, block2 = content.split('\n\n')

    workflows = {}
    for line in block1.splitlines():
        name, conditions = line.rstrip('}').replace('{', ' ').split()
        workflows[name] = [parse_condition(txt) for txt in conditions.split(',')]

    parts = []
    for line in block2.splitlines():
        part = {}
        for item in line.strip('{}').split(','):

            p, val = item.split('=')
            part[p] = int(val)
        parts.append(part)
    return workflows, parts


def play(part, workflows):
    current = 'in'
    while True:
        for cond in workflows[current]:
            res = None
            if cond[0] == 0:
                res = cond[1]
            elif cond[0] == 1 and part[cond[1]] < cond[2]:
                res = cond[3]
            elif cond[0] == 2 and part[cond[1]] > cond[2]:
                res = cond[3]
            if res == 'A':
                return True
            elif res == 'R':
                return False
            elif res is not None:
                current = res
                break


def play_range(current, state, workflows, icond=0):
    M.debug('call %s : %s', current, state)
    if current == 'A':
        res = 1
        for r in state.values():
            res *= r[1] - r[0] + 1
        M.debug('ACCEPTED %s', list(state.values()))
        return res
    elif current == 'R':
        return 0

    res = 0
    cond = workflows[current][icond]

    if cond[0] == 0:
        M.debug('case0')
        res += play_range(cond[1], state, workflows)
    elif cond[0] == 1:
        M.debug('case1 (part<val) %s, %s', cond, state)
        r = state[cond[1]]
        if r[0] < cond[2]:
            if r[1] < cond[2]:
                M.debug('case1all')
                res += play_range(cond[3], state, workflows)
            else:
                M.debug('case1split')
                ns = state.copy()
                ns[cond[1]] = (r[0], cond[2] - 1)
                res += play_range(cond[3], ns, workflows)
                ns[cond[1]] = (cond[2], r[1])
                res += play_range(current, ns, workflows, icond=icond+1)
        else:
            res += play_range(current, state, workflows, icond=icond+1)

    elif cond[0] == 2:
        M.debug('case2 (part>val) %s, %s', cond, state)
        r = state[cond[1]]
        if r[1] > cond[2]:
            if r[0] > cond[2]:
                M.debug('case2all')
                res += play_range(cond[3], state, workflows)
            else:
                M.debug('case2split')
                ns = state.copy()
                ns[cond[1]] = (r[0], cond[2])
                M.debug('%s %s', current, ns)
                res += play_range(current, ns, workflows, icond=icond+1)
                ns[cond[1]] = (cond[2] + 1, r[1])
                res += play_range(cond[3], ns, workflows)
        else:
            res += play_range(current, state, workflows, icond=icond+1)
    return res


@M.timeperf
def test():
    M.log()
    workflows, parts = load_input('input_test')
    print(workflows)
    print(parts)
    M.nolog()
    for part in parts:
        print(part, play(part, workflows))
        print(part, play_range('in', {k: (v, v) for k, v in part.items()}, workflows))


@M.timeperf
def part1():
    M.nolog()
    workflows, parts = load_input('input')
    res = 0
    for part in parts:
        if play(part, workflows):
            res += sum(part.values())
    print('part1', res)


@M.timeperf
def part2():
    M.nolog()
    workflows, parts = load_input('input')
    print(play_range('in', {k: (1, 4000) for k in 'xmas'}, workflows))
    print('part2')


if __name__ == '__main__':
    test()
    part1()
    part2()
