import numpy as np
import itertools

def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            actiontxt, boxtxt = line.strip().split(' ', maxsplit=1)

            action = 1 if actiontxt == 'on' else 0

            axes = boxtxt.split(',')
            box = []
            for a in axes:
                dims = a.split('=')[1].split('.')
                box.append((int(dims[0]), int(dims[-1])))

            res.append({'action': action, 'box': box})
    return res


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def empty(self):
        return self.a > self.b

    def center(self):
        return int((self.b + self.a)/2)

    def size(self):
        return self.b - self.a + 1

    def inside(self, x):
        return self.a <= x and self.b >= x

    def intersect(self, line):
        newb = min(self.b, line.b)
        newa = max(self.a, line.a)

        if newa > newb:
            return None

        return Line(newa, newb)

    def include(self, line):
        return self.a <= line.a and self.b >= line.b

    def split_intersect(self, line):
        intersect = self.intersect(line)
        if intersect is None:
            return None

        return [
            Line(min(self.a, line.a), intersect.a - 1),
            intersect,
            Line(intersect.b + 1, max(self.b, line.b))]

    def list(self):
        return [self.a, self.b]

    def __repr__(self):
        return 'Line({0:.0f},{1:.0f})'.format(self.a, self.b)

    def translate(self, dd):
        self.a += dd
        self.b += dd


class Box:
    def __init__(self, x, y, z):
        self.x = Line(*x)
        self.y = Line(*y)
        self.z = Line(*z)

    def empty(self):
        return self.x.empty() or self.y.empty() or self.z.empty()

    def size(self):
        return self.x.size() * self.y.size() * self.z.size()

    def inside(self, x, y, z):
        return self.x.inside(x) and self.y.inside(y) and self.z.inside(z)

    def include(self, box):
        return self.x.include(box.x) and self.y.include(box.y) and self.z.include(box.z)

    def center(self):
        return self.x.center(), self.y.center(), self.z.center()

    def copy(self):
        return Box(self.x.list(), self.y.list(), self.z.list())

    def intersect(self, box):
        lx = self.x.intersect(box.x)
        if lx is None:
            return None
        ly = self.y.intersect(box.y)
        if ly is None:
            return None
        lz = self.z.intersect(box.z)
        if lz is None:
            return None
        return Box(lx.list(), ly.list(), lz.list())

    def split_intersect(self, box):
        intersection = self.intersect(box)
        if intersection is None:
            return None

        xlines = self.x.split_intersect(box.x)
        ylines = self.y.split_intersect(box.y)
        zlines = self.z.split_intersect(box.z)

        boxes = []
        for ix, iy, iz in itertools.product([0, 1, 2], repeat=3):
            b = Box(xlines[ix].list(), ylines[iy].list(), zlines[iz].list())
            boxes.append(b)

        return boxes

    def union(self, box):
        boxes = self.split_intersect(box)
        if boxes is None:
            return None

        union = []
        for b in boxes:
            if b.empty():
                continue
            center = b.center()
            if self.inside(*center) or box.inside(*center):
                union.append(b)
        return union

    def remaining(self, box):
        boxes = self.split_intersect(box)
        if boxes is None:
            return None

        remaining = []
        for b in boxes:
            if b.empty():
                continue
            center = b.center()
            if not self.inside(*center) and box.inside(*center):
                remaining.append(b)
        return remaining

    def difference(self, box):
        boxes = self.split_intersect(box)
        if boxes is None:
            return None

        difference = []
        for b in boxes:
            if b.empty():
                continue
            center = b.center()
            if self.inside(*center) and not box.inside(*center):
                difference.append(b)
        return difference

    def translate(self, dx, dy, dz):
        self.x.translate(dx)
        self.y.translate(dy)
        self.z.translate(dz)

    def __repr__(self) -> str:
        return 'Box[X{0},Y{1},Z{2}]'.format(self.x, self.y, self.z)


def part1():
    res = load_input('input')

    boxRef = Box([-50, 50], [-50, 50], [-50, 50])

    delta = 50
    size = delta * 2 + 1

    for elem in res:
        b = elem['box']
        intersection = Box(b[0], b[1], b[2]).intersect(boxRef)
        if intersection is not None:
            intersection.translate(50, 50, 50)
        elem['box'] = intersection

    for elem in res:
        print(elem)

    grid = np.zeros((size, size, size))

    for elem in res:
        if elem['box'] is None:
            continue
        val = elem['action']
        grid[
            elem['box'].x.a:elem['box'].x.b+1,
            elem['box'].y.a:elem['box'].y.b+1,
            elem['box'].z.a:elem['box'].z.b+1
        ] = val

    print(np.sum(grid == 1))


def test():
    a = Box([0, 10], [0, 10], [0, 10])
    b = Box([5, 15], [5, 15], [5, 15])

    u = a.union(b)
    print('*union', len(u))
    for box in u:
        print(box)

    d = a.difference(b)
    d = Box([1, 5], [1, 5], [1, 5]).difference(Box([0, 10], [0, 10], [0, 10]))
    print('*difference', len(d))
    for box in d:
        print(box)

    op = a.remaining(b)
    print('*remaining', len(op))
    for box in op:
        print(box)


def part2():
    res = load_input('input')
    for elem in res:
        b = elem['box']
        intersection = Box(b[0], b[1], b[2])
        elem['box'] = intersection

    partition = []

    for elem in res:
        if elem['action'] == 1:
            print('* union', elem['box'])
            current = [elem['box'].copy()]

            # print('partition size', len(partition))
            for part in partition:
                newcurrent = []
                if len(current) == 0:
                    break
                # print('split', len(current))
                for remain in current:
                    if part.include(remain):
                        continue
                    res = part.remaining(remain)
                    if res is not None:
                        newcurrent.extend(res)
                    else:
                        newcurrent.append(remain)
                current = newcurrent
            # print('add to partition ', len(current))
            partition.extend(current)
        else:
            print('* remove', elem['box'])
            newpartition = []
            for part in partition:
                diff = part.difference(elem['box'])
                if diff is None:
                    newpartition.append(part)
                else:
                    newpartition.extend(diff)
            partition = newpartition

    area = 0
    for box in partition:
        # print(box, box.size())
        area += box.size()
    print(len(partition))
    print(area)


if __name__ == '__main__':
    # test()
    # part1()
    part2()

