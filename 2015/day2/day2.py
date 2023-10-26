def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            l, w, h = line.strip().split('x')
            res.append((int(l), int(w), int(h)))
    return res


if __name__ == '__main__':
    presents = load_input('input')

    part1 = 0
    part2 = 0
    for p in presents:
        l, w, h = p

        s = 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)
        part1 += s

        p = 2 * min(l+w, w+h, h+l) + l*w*h
        part2 += p
    
    print('part1', part1)
    print('part2', part2)

