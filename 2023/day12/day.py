import pycommon as M
import itertools
from functools import lru_cache


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            spring, groups = line.split()
            groups = M.ints_txt(groups)
            res.append((spring, tuple(groups)))

    return res


def search_choices(spring):
    ls = list(spring)
    indice = [i for i in range(len(spring)) if spring[i] == '?']

    for choice in itertools.product('.#', repeat=len(indice)):
        for i, c in zip(indice, choice):
            ls[i] = c

        yield ''.join(ls)


def search_choices2(spring, groups):
    damaged = sum(groups)
    ls = list(spring)
    count_damaged = len([i for i in range(len(spring)) if spring[i] == '#'])
    indice = [i for i in range(len(spring)) if spring[i] == '?']
    ls_ok = [e if e == '#' else '.' for e in ls]

    count = 0
    for choice in itertools.combinations(indice, damaged - count_damaged):
        newls = ls_ok.copy()
        for i in choice:
            newls[i] = '#'
        res = ''.join(newls)
        test = count_contiguous(res) == groups
        M.debug('check %s: %s', res, test)
        count += int(test)
    return count


@lru_cache(maxsize=2**20)
def search_choices3(spring, groups, ingrp=False):
    M.debug('check %s, %s, %s', spring, groups, ingrp)
    if not groups:
        for c in spring:
            if c == "#":
                M.debug('no')
                return 0
        M.debug('ok1')
        return 1

    if len(spring) == 0 and groups:
        M.debug('no')
        return 0

    if ingrp:
        if spring[0] == '.':
            M.debug('no')
            return 0
        if spring[0] == '#':
            g = groups[0] - 1
            if g == 0:
                if len(spring) > 1 and spring[1] in '.?':
                    return search_choices3(spring[2:], groups[1:], False)
                elif len(groups) > 1:
                    M.debug('no')
                    return 0
                else:
                    M.debug('ok2' if len(spring) == 1 else 'not')
                    return int(len(spring) == 1)
            else:
                return search_choices3(spring[1:], (g,) + groups[1:], True)
        elif spring[0] == '?':
            g = groups[0]
            if g > 0:
                return search_choices3('#' + spring[1:], groups, True)
            else:
                return search_choices3(spring[1:], groups, False)
    else:
        if spring[0] == '.':
            return search_choices3(spring.lstrip('.'), groups, False)
        elif spring[0] == '#':
            return search_choices3(spring, groups, True)
        else:
            c1 = search_choices3(spring[1:].lstrip('.'), groups, False)
            c2 = search_choices3('#' + spring[1:], groups, False)
            return c1 + c2


def count_contiguous(spring):
    return tuple([len(e) for e in spring.split('.') if len(e) > 0])


@M.timeperf
def test():
    M.nolog()
    data = load_input('input_test')
    print(data)
    for row in data:
        print(row[0], count_contiguous(row[0]), len(list(search_choices(row[0]))))
        print(
            row[0],
            search_choices2(row[0], row[1]),
            search_choices3(row[0], row[1]))

    M.log()
    spring = '?###????????'
    ref_count = (3, 2, 1)
    print('*study', spring, ref_count)
    print(search_choices3(row[0], row[1]))


@M.timeperf
def part1():
    M.nolog()
    data = load_input('input')
    total = 0
    for spring, ref_count in data:
        total += (count := search_choices3(spring, ref_count))
        M.debug("%s = %s", spring, count)
    print('part1', total)


@M.timeperf
def part2():
    M.nolog()
    data = load_input('input')
    total = 0
    pcache = search_choices3.cache_info()
    for spring, ref_count in data:
        s = f'{spring}?{spring}?{spring}?{spring}?{spring}'
        r = ref_count + ref_count + ref_count + ref_count + ref_count
        t2 = search_choices3(s, r)
        total += t2
        cache = search_choices3.cache_info()
        cache_call = (cache.hits - pcache.hits + cache.misses - pcache.misses)
        cache_ratio = 100 * (cache.hits - pcache.hits) / cache_call
        pcache = cache

        print(spring, '  ', ref_count, '=', t2, f', cache_usage {int(cache_ratio)}% of {cache_call} calls,', 'cache size', cache.currsize)
    print('part2', total)


if __name__ == '__main__':
    # test()
    part1()
    part2()
