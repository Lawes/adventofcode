import sys
from itertools import combinations, permutations

class Element(object):
    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None
        self.value = None


def split_token(txt):
    pos = 0
    level = 0
    cur = ''

    tokens = []

    while pos < len(txt):
        if level == 0 and txt[pos] == ',':
            tokens.append(cur)
            cur = ''
        else:
            cur += txt[pos]
            if txt[pos] == '[':
                level += 1
            elif txt[pos] == ']':
                level -= 1

        pos += 1

    if len(cur) > 0:
        tokens.append(cur)

    if len(tokens) == 1:
        token = tokens[0]
        if token[0] in '0123456789':
            content = int(token)
        elif token[0] == '[' and token[-1] == ']':
            content = split_token(token[1:-1])
    else:
        content = tokens

    return content


def tokenize(txt):
    tokens = split_token(txt)

    if isinstance(tokens, int):
        return tokens

    return [tokenize(tokens[0]), tokenize(tokens[1])]


def create_graph(main, tokens):
    node = Element()
    node.parent = main
    if isinstance(tokens, list):
        node.left = create_graph(node, tokens[0])
        node.right = create_graph(node, tokens[1])
    else:
        node.value = tokens
    return node


def check_nested_pair(g, lvl=0):
    node = g
    check = False
    if g.value is not None:
        pass
    elif lvl >= 4:
        #print('explode')
        tnode = left(g)
        if tnode is not None:
            #print('sum', tnode.value, g.left.value, '(', id(tnode))
            tnode.value += g.left.value
        tnode = right(g)
        if tnode is not None:
            #print('sum', tnode.value, g.right.value, '(', id(tnode))
            tnode.value += g.right.value
        node = Element()
        node.value = 0
        node.parent = g.parent
        check = True
    else:
        g.left, check = check_nested_pair(g.left, lvl + 1)
        if not check:
            g.right, check = check_nested_pair(g.right, lvl + 1)

    return node, check


def check_10(g):
    node = g
    check = False
    if g.value is None:
        g.left, check = check_10(g.left)
        if not check:
            g.right, check = check_10(g.right)
    elif g.value is not None:
        if g.value >= 10:
            check = True
            node = Element()
            node.parent = g.parent

            v1 = int(float(g.value)/2)
            v2 = int(float(g.value)/2 + 0.5)
            g.value = None
            n = Element()
            n.parent = node
            n.value = v1
            node.left = n
            n = Element()
            n.parent = node
            n.value = v2
            node.right = n


    return node, check


def reduce_graph(g):
    check = True
    while check:
        g, c1 = check_nested_pair(g)
        if c1:
            continue
        g, c2 = check_10(g)
        check = c1 or c2

    return g


def add(g1, g2):
    node = Element()
    g1.parent = node
    g2.parent = node
    node.left = g1
    node.right = g2

    return node


def left(g):
    node = g
    while True:
        if node.parent is None:
            return None
        if id(node.parent.left) != id(node):
            break
        node = node.parent

    node = node.parent.left

    while node.value is None:
        node = node.right

    return node


def right(g):
    node = g
    while True:
        if node.parent is None:
            return None
        if id(node.parent.right) != id(node):
            break
        node = node.parent

    node = node.parent.right

    while node.value is None:
        node = node.left

    return node


def magnitude(g):
    if g.value is not None:
        return g.value
    return 3*magnitude(g.left) + 2*magnitude(g.right)


def display_graph(g, lvl=1):
    if g.value is not None:
        print(' '*lvl, '> value', g.value, id(g))
    else:
        print(' '*lvl, '> node', id(g))  # , g.parent is None, id(g.parent))  # , 'left', left(g), 'right', right(g))
        display_graph(g.left, lvl+4)
        display_graph(g.right, lvl+4)


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            res.append(line.strip())
    return res


if __name__ == '__main__':
    """
    for e in ['[[[5,[7,11]],8],1]', '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]']:  # , '[[1,2],[3,4]]', '[[[[8,3],0],[[4,8],[7,9]]],[[7,1],[[8,4],[4,4]]]]']:
        print('-', tokenize(e))
        graph = create_graph(None, tokenize(e))
        display_graph(graph)
        print(' *check')
        # g, check = check_pair(graph)
        reduce_graph(graph)
        print('**** reduce ****')
        display_graph(graph)

    n1 = '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]'
    n2 = '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]'
    g1 = create_graph(None, tokenize(n1))
    g2 = create_graph(None, tokenize(n2))

    a = add(g1, g2)
    print('***before')
    display_graph(a)
    reduce_graph(a)
    print('***result')
    display_graph(a)
    print('magnitude', magnitude(a))

    sys.exit(0)
    """
    data = load_input('input4')
    data = [create_graph(None, tokenize(e)) for e in data]
    sum = data[0]
    for g in data[1:]:
        print('**** new data')
        display_graph(sum)
        print('*** add with ')
        display_graph(g)
        t = add(sum, g)
        reduce_graph(t)
        sum = t

    print('**** final sum') 
    display_graph(sum)
    print('part1', magnitude(sum))

    data = load_input('input')
    mag = []
    for i1 in range(len(data)):
        for i2 in range(len(data)):
            if i1 == i2:
                continue
            print('*', i1, i2)
            s = add(create_graph(None, tokenize(data[i1])), create_graph(None, tokenize(data[i2])))
            reduce_graph(s)
            print(magnitude(s))
            mag.append(magnitude(s))

    print('part2', max(mag))