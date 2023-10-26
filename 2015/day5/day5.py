
from collections import Counter

def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            res.append(line.strip())
    return res


def has_double(txt):
    return sum(l1 == l2 for l1, l2 in zip(txt[:-1], txt[1:])) > 0


def is_nice(txt):
    c = Counter(txt)
    hasVowel = sum([c[vowel] for vowel in 'aeiou']) > 2
    hasDouble = has_double(txt)
    hasBlacklist = sum(txt.find(pattern)>-1 for pattern in ['ab', 'cd', 'pq', 'xy']) > 0

    return hasVowel and hasDouble and not hasBlacklist


def has_non_overlapping_pair(txt):
    for i in range(len(txt)-1):
        if txt[i]+txt[i+1] in txt[i+2:]:
            return True
    return False

def is_nice2(txt):

    hasXYX = has_double(txt[::2]) or has_double(txt[1::2])

    return hasXYX and has_non_overlapping_pair(txt)


if __name__ == '__main__':

    for test in ['ugknbfddgicrmopn', 'aaa', 'jchzalrnumimnmhp', 'haegwjzuvuyypxyu', 'dvszwmarrgswjxmb']:
        print(test, is_nice(test))

    data = load_input('input')

    print('part1', sum([is_nice(txt) for txt in data]))

    for test in ['qjhvhtzxzqqjkmpb', 'xxyxx', 'uurcxstgmygtbstg', 'ieodomkazucvgmuy', 'aaa']:
        print(test, is_nice2(test))

    print('part2', sum([is_nice2(txt) for txt in data]))