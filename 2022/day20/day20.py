
def load_input(filename):
    with open(filename, 'r') as f:
        res = [int(e) for e in f]
    print('load', len(res), 'elements.')
    return res


class Node:
    def __init__(self, v):
        self.val = v
        self.gauche = None
        self.droite = None


def create_doublelinked(seq):
    nodeseq = [Node(elem) for elem in seq]
    zero = None

    for i, node in enumerate(nodeseq):
        if node.val == 0:
            zero = node
        node.gauche = nodeseq[i - 1]
        node.droite = nodeseq[(i + 1)%len(nodeseq)]
    return nodeseq, zero


def advanceto(node, dist, n):
    current = node
    if dist > 0:
        for i in range(dist%(n - 1)):
            current = current.droite
    elif dist < 0:
        for i in range((-dist+1)%(n - 1)):
            current = current.gauche
    return current


def tolist(node, n):
    l = []
    current = node
    for i in range(n):
        l.append(current.val)
        current = current.droite
    return l


def mix(nodeseq):
    for n in nodeseq:
        destn = advanceto(n, n.val, len(nodeseq))

        if id(destn) == id(n):
            continue

        n.gauche.droite = n.droite
        n.droite.gauche = n.gauche

        n.gauche = destn
        n.droite = destn.droite

        destn.droite.gauche = n
        destn.droite = n


def test():
    seq = load_input('input_test')

    nodeseq, zero = create_doublelinked(seq)

    print(seq)

    mix(nodeseq)

    print(tolist(nodeseq[0], len(nodeseq)))


def part1():
    seq = load_input('input')
    nodeseq, zero = create_doublelinked(seq)
    mix(nodeseq)

    print('part1', sum([advanceto(zero, d, len(nodeseq)).val for d in [1000, 2000, 3000]]))


def part2():
    seq = load_input('input')
    nodeseq, zero = create_doublelinked(seq)

    for n in nodeseq:
        n.val *= 811589153

    for i in range(10):
        mix(nodeseq)

    print('part2', sum([advanceto(zero, d, len(nodeseq)).val for d in [1000, 2000, 3000]]))


if __name__ == '__main__':

    part2()
