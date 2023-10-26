
from collections import Counter, defaultdict


def load_input(filename):
    with open(filename, 'r') as f:
        line = next(f).rstrip()
    population = [int(e) for e in line.split(',')]
    return population


if __name__ == '__main__':
    pop = load_input('input')
    print(pop)

    pop = Counter(pop)

    for day in range(256):
        newgen = defaultdict(int)

        for age, num in pop.items():
            if age == 0:
                newgen[6] += num
                newgen[8] += num
            else:
                newgen[age-1] += num

        pop = newgen
        # print(day+1, pop)

    print(sum(pop.values()))
