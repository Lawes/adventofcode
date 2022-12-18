
def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            dir, n = line.split()
            res.append((dir, int(n)))
    return res


def move_head(head, dir):
    x, y = head
    if dir == 'U':
        return x, y+1
    if dir == 'D':
        return x, y-1
    if dir == 'L':
        return x-1, y

    return x+1, y


def clamp(x):
    return min(max(x, -1), 1)


def move_tail(head, tail):
    xh, yh = head
    xt, yt = tail
    dx, dy = xh - xt, yh - yt

    if max(abs(dx), abs(dy)) > 1:
        xt = xt + clamp(dx)
        yt = yt + clamp(dy)

    return xt, yt


def step(head, tail, dir, n):
    poshead = []
    postail = []
    for _ in range(n):
        head = move_head(head, dir)
        poshead.append(head)
        tail = move_tail(head, tail)
        postail.append(tail)
    return head, tail, poshead, postail


def step_rope(knots, dir, n):
    postail = []
    newknots = knots.copy()
    for _ in range(n):
        newknots[0] = move_head(newknots[0], dir)
        for ik in range(1, 10):
            newknots[ik] = move_tail(newknots[ik-1], newknots[ik])
        postail.append(newknots[9])
    return newknots, postail


def displaygrid(size, pos):
    g = [[0] * size for _ in range(size)]

    for p in pos:
        g[p[1]][p[0]] = 1

    for row in g:
        print(row)


if __name__ == '__main__':

    moves = load_input('input')

    head = (0, 0)
    tail = (0, 0)

    head, tail, _, pos = step(head, tail, 'R', 2)
    print(head, tail, pos)

    head = (0, 0)
    tail = (0, 0)

    postail = [tail]
    for m in moves:
        # print('=======')
        head, tail, _, pos = step(head, tail, m[0], m[1])
        # displaygrid(6, pos)
        postail.extend(pos)

    print('part1', len(set(postail)))

    knots = [(0, 0) for i in range(10)]
    postail = [(0, 0)]
    for m in moves:
        knots, pos = step_rope(knots, m[0], m[1])
        postail.extend(pos)
    print('part1', len(set(postail)))
