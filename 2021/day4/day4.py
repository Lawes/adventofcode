
class Carton(object):
    def __init__(self, n):
        self.data = []
        self.mask = []
        for _ in range(n):
            self.mask.append([0] * n)
        self.size = n

    def add_line(self, line):
        self.data.append(line[:self.size])

    def wins(self):
        for line in self.mask:
            if sum(line) == self.size:
                return True

        for line in list(zip(*self.mask)):
            if sum(line) == self.size:
                return True

        return False

    def unmarked(self):
        res = []
        for ir in range(self.size):
            for ic in range(self.size):
                if self.mask[ir][ic] == 0:
                    res.append(self.data[ir][ic])
        return res

    def mark(self, num):
        for ir, row in enumerate(self.data):
            for ic, elem in enumerate(row):
                if elem == num:
                    self.mask[ir][ic] = 1
        return self

    def __repr__(self):
        return '-'.join((','.join([str(e) for e in line]) for line in self.data))


def load_input(filename):
    res = []
    with open(filename, 'r') as f:
        tirage = [int(e) for e in next(f).rstrip().split(',')]

        curCarton = None
        for line in f:
            line = line.strip()
            if len(line) == 0:
                if curCarton is not None:
                    res.append(curCarton)
                curCarton = Carton(5)
            else:
                curCarton.add_line([int(e) for e in line.rstrip().split()])

    return {'tirage': tirage, 'cartons': res}


if __name__ == '__main__':
    data = load_input('input')

    res = None
    nowin = data['cartons']
    for num in data['tirage']:
        temp = []
        for c in nowin:
            c.mark(num)
            if not c.wins():
                temp.append(c)
        if len(temp) == 0:
            res = nowin[0], num
            break
        nowin = temp


    wining, lastnum = res

    print('res', sum(wining.unmarked()) * lastnum)
