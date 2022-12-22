import re

_intpattern = re.compile(r'-?\d+')


def ints_txt(txt):
    return [int(m) for m in _intpattern.findall(txt)]


def ints_file(filename):
    with open(filename, 'r') as f:
        return [ints_txt(line) for line in f]
