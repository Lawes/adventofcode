def load_input(filename):
    res = []
    east = []
    south = []
    with open(filename, 'r') as f:
        for ix, line in enumerate(f):
            row = []
            for iy, cell in enumerate(line.strip()):
                c = 0
                if cell == '>':
                    c = 1
                    east.append((ix, iy))
                elif cell == 'v':
                    c = 2
                    south.append((ix, iy))

                row.append(c)
            res.append(row)
    return res, east, south


class SeaFloor:
    def __init__(self, grid):
        self.grid = grid
        self.nx = len(grid)
        self.ny = len(grid[0])

    def isEastFree(self, ix, iy):
        check = iy + 1
        if check >= self.ny:
            check = 0
        test = self.grid[ix][check] == 0
        if not test:
            check = iy

        return test, (ix, check)

    def isSouthFree(self, ix, iy):
        check = ix + 1
        if check >= self.nx:
            check = 0
        
        test = self.grid[check][iy] == 0
        if not test:
            check = ix

        return test, (check, iy)

    def display(self):
        for ix in range(self.nx):
            txt = ''
            for iy in range(self.ny):
                v = self.grid[ix][iy]
                if v == 1:
                    txt += '>'
                elif v == 2:
                    txt += 'v'
                else:
                    txt += '.'
            print(txt)

    def move_east(self):
        newgrid = []
        oneMove = False
        for ix in range(self.nx):
            newgrid.append([0] * self.ny)

        for ix in range(self.nx):
            for iy in range(self.ny):
                v = self.grid[ix][iy]
                if v == 1:
                    check, pos = self.isEastFree(ix, iy)
                    if check:
                        oneMove = True
                    newgrid[pos[0]][pos[1]] = 1
                elif v == 2:
                    newgrid[ix][iy] = 2

        self.grid = newgrid
        return oneMove

    def move_south(self):
        newgrid = []
        oneMove = False
        for ix in range(self.nx):
            newgrid.append([0] * self.ny)

        for ix in range(self.nx):
            for iy in range(self.ny):
                v = self.grid[ix][iy]
                if v == 2:
                    check, pos = self.isSouthFree(ix, iy)
                    if check:
                        oneMove = True
                    newgrid[pos[0]][pos[1]] = 2
                elif v == 1:
                    newgrid[ix][iy] = 1
        self.grid = newgrid
        return oneMove

    def step(self):

        hasMoved1 = self.move_east()
        hasMoved2 = self.move_south()

        return hasMoved1 or hasMoved2



if __name__ == '__main__':
    grid, east, south = load_input('input')


    sf = SeaFloor(grid)
    sf.display()

    step = 0
    while True:
        step += 1
        # print('*', step)

        hasMoved = sf.step()
        # sf.display() 
        if not hasMoved:
            break
    print(step)

