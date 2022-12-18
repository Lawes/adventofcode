
def load_input(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    return data


class Node:
    def __init__(self, name, parent, size=-1):
        self.name = name
        self.parent = parent
        self.size = size
        self.fils = []

    def __repr__(self):
        ftxt = '-'.join(f.name for f in self.fils)
        return f'{self.name}({ftxt})'

    def add(self, *args, **kwargs):
        self.fils.append(Node(*args, **kwargs))

    def find(self, name):
        for n in self.fils:
            if n.name == name:
                return n
        return None


def affiche(node, prefix=''):
    print(prefix + '-', node.name, ':', node.size if node.size > 0 else '')
    for f in node.fils:
        affiche(f, prefix=prefix + '    ')


def du(node, res):
    if node.size > 0:
        return node.size

    total = 0
    for f in node.fils:
        total += du(f, res)

    res.append((node.name, total))
    return total


class Tree:
    def __init__(self):
        self.tree = Node('/', None)
        self.current = self.tree

    def curr(self):
        return self.current

    def cd(self, name):
        if name == '..':
            self.current = self.current.parent
        else:
            n = self.current.find(name)
            if n is None:
                self.current.add(name, self.current)
            self.current = n


if __name__ == '__main__':

    cmds = load_input('input_test')

    tree = Tree()
    isok = True
    for line in cmds[1:]:
        tokens = line.strip().split()
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                tree.cd(tokens[2])
        else:
            curr = tree.curr()
            n = curr.find(tokens[1])
            if n is None:
                if tokens[0] == 'dir':
                    curr.add(tokens[1], curr)
                else:
                    curr.add(tokens[1], curr, size=int(tokens[0]))
        # print(line.strip(), ':', tree.curr())
    affiche(tree.tree)

    res = []
    total = du(tree.tree, res)
    part1 = 0
    for name, size in res:
        if size <= 100000:
            part1 += size
    print('part1', part1)

    maxsize = 40000000
    torm = []
    for k, v in res:
        if total - v < maxsize:
            torm.append((v, k))

    print(torm)
    print('part2', min(torm)[0])
