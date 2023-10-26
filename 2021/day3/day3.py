from collections import Counter


def load_input(filename):
    data = []
    with open(filename, 'r') as f:
        for l in f:
            data.append([int(e) for e in l.rstrip()])
    return data


def convert_bin(array):
    num = 0
    for i, v in enumerate(array[::-1]):
        num += v * pow(2, i)
    return num

if __name__ == '__main__':
    records = load_input('input')

    perbits = list(zip(*records))[::-1]

    # part 1
    gamma = 0
    epsilon = 0
    for i, bits in enumerate(perbits):
        c = Counter(bits)
        if c[1] > c[0]:
            gamma += pow(2, i)
        else:
            epsilon += pow(2, i)

    print('gamma', gamma)
    print('epsilon', epsilon)
    print('power', gamma * epsilon)


    # part 2
    n = len(records[0])

    o2 = records.copy()
    for i in range(n):
        bits = Counter([e[i] for e in o2])
        most = 1 if bits[1] >= bits[0] else 0

        o2 = [e for e in o2 if e[i] == most]

        if len(o2) == 1:
            break

    co2 = records.copy()
    for i in range(n):
        bits = Counter([e[i] for e in co2])
        least = 0 if bits[0] <= bits[1] else 1

        co2 = [e for e in co2 if e[i] == least]

        if len(co2) == 1:
            break

    o2 = o2[0]
    co2 = co2[0]
    print(o2, co2)
    o2_rate = convert_bin(o2)
    print('O2', o2, o2_rate)
    co2_rate = convert_bin(co2)
    print('CO2', co2, co2_rate)

    print('life', o2_rate * co2_rate)

