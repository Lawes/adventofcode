
def load_input(filename):
    pts = []
    with open(filename, 'r') as f:
        for line in f:
            pts.append(tuple(int(e) for e in line.split(',')))
    return pts


def distance(pt1, pt2):
    return sum(abs(e1 - e2) for e1, e2, in zip(pt1, pt2))


def test():
    pts = load_input('input_test')
    print(pts)

    total = 0
    for pt1 in pts:
        print(pt1, [distance(pt1, pt2)for pt2 in pts])
        voisins = sum(distance(pt1, pt2) == 1 for pt2 in pts)
        print(pt1, voisins)
        total += max(6 - voisins, 0)
    print('test', total)


def part1():
    pts = load_input('input')

    total = 0
    for pt1 in pts:
        voisins = sum(distance(pt1, pt2) == 1 for pt2 in pts)
        total += 6 - voisins
    print('part1', total)


def part2():
    pts = load_input('input')

    allx, ally, allz = list(zip(*pts))

    xrange = [min(allx)-1, max(allx)+1]
    yrange = [min(ally)-1, max(ally)+1]
    zrange = [min(allz)-1, max(allz)+1]

    obsidian = set(pts)
    contact = set()
    exterior = set()
    openlist = set([(xrange[0], yrange[0], zrange[0])])

    while openlist:
        newopenlist = set()
        for pt in openlist:
            for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                check = (pt[0] + dx, pt[1] + dy, pt[2] + dz)
                if check in obsidian:
                    contact.add(pt)
                elif not (xrange[0] <= check[0] <= xrange[-1] and yrange[0] <= check[1] <= yrange[-1] and zrange[0] <= check[2] <= zrange[-1]):
                    pass
                elif check not in exterior and check not in openlist and check not in newopenlist:
                    newopenlist.add(check)
            exterior.add(pt)
        openlist = newopenlist

    total = sum(sum(distance(pt1, pt2) == 1 for pt2 in pts) for pt1 in contact)
    print('part2', total)


if __name__ == '__main__':
    part2()

