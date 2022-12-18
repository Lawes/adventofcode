
def load_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return data



if __name__ == '__main__':

    data = load_input('input')

    elves = []
    current = 0
    for entry in data:
        if entry:
            current += int(entry)
        else:
            elves.append(current)
            current = 0

    if current > 0:
        elves.append(current)

    print('part1', max(elves))

    elves.sort()
    print(elves[-3:])
    print('part2', sum(elves[-3:]))
