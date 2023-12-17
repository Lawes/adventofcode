import re

_intpattern = re.compile(r'-?\d+')


def ints_txt(txt):
    return [int(m) for m in _intpattern.findall(txt)]


def ints_file(filename):
    with open(filename, 'r') as f:
        return [ints_txt(line) for line in f]


def grid_txt(txt, mapping):
    grid = {}
    content = txt.splitlines()
    ny = len(content)
    if ny == 0:
        return grid, 0, 0
    nx = len(content[0])
    for iy, line in enumerate(content):
        for ix, c in enumerate(line):
            val = mapping.get(c)
            if val is not None:
                grid[(ix, iy)] = val
    return grid, nx, ny


def grid_file(filename, mapping):
    with open(filename, 'r') as f:
        return grid_txt(f.read(), mapping)
