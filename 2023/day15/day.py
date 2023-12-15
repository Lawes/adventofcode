import pycommon as M
from collections import Counter, defaultdict


def load_input(filename):
    with open(filename, 'r') as f:
        content = f.read().rstrip()
    return content.split(',')


def myhash(txt):
    res = 0
    for c in txt:
        res = ((res + ord(c)) * 17) % 256
        M.debug(res)
    return res


@M.timeperf
def test():
    M.log()
    data = load_input('input_test')
    print(sum([myhash(e) for e in data]))


@M.timeperf
def part1():
    M.nolog()
    data = load_input('input')
    print('part1', sum([myhash(e) for e in data]))

    count = Counter()
    for inst in data:
        if '-' in inst:
            count['-'] += 1
        elif '=' in inst:
            count['='] += 1
    # just to know how many set and remove
    print(count)


@M.timeperf
def part2():
    data = load_input('input')

    boxes = defaultdict(list)

    for instruction in data:
        if '=' in instruction:
            label, val = instruction.split('=')

            ibox = myhash(label)
            isFound = False
            for lens in boxes[ibox]:
                if label == lens[0]:
                    lens[1] = int(val)
                    isFound = True
                    break

            if not isFound:
                boxes[ibox].append([label, int(val)])
        elif '-' in instruction:
            label = instruction[:-1]
            ibox = myhash(label)
            torm = None
            alllens = boxes[ibox]
            for i in range(len(alllens)):
                lens = alllens[i]
                if label == lens[0]:
                    torm = i
                    break
            if torm is not None:
                del alllens[torm]

    res = 0
    for ibox, llens in boxes.items():
        for islot, lens in enumerate(llens):
            res += (ibox + 1) * (islot + 1) * lens[1]

    print('part2', res)


if __name__ == '__main__':
    test()
    part1()
    part2()
