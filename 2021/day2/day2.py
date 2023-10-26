def load_input(filename):
    data = []
    with open(filename, 'r') as f:
        for l in f:
            action, val = l.rstrip().split()
            data.append((action, int(val)))
    return data


if __name__ == '__main__':
    records = load_input('input')

    xpos = 0
    depth = 0
    aim = 0

    for a, v in records:
        if a == 'forward':
            xpos += v
            depth += aim * v
        elif a == 'down':
            aim += v
        elif a == 'up':
            aim -= v
    
    print('position:', xpos, 'depth:', depth)
    print('result:', xpos * depth)


