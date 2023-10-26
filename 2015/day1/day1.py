from collections import Counter


def load_input(filename):
    with open(filename, 'r') as f:
        line = next(f).rstrip()
    return line


if __name__ == '__main__':
    actions = load_input('input')

    d = Counter(actions)

    print(d['('] - d[')'])

    pos = 0
    for indice, a in enumerate(actions):
        if a == '(':
            pos += 1
        elif a == ')':
            pos -= 1

        if pos == -1:
            print('basement', indice+1)
            break
