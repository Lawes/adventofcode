import numpy as np
import sys


def load_input():
    return [217, 240], [-126, -69]


def shot_step(x0, y0, v0x, v0y):
    x = x0 + v0x
    y = y0 + v0y
    if v0x > 0:
        vx = v0x - 1
    elif v0x < 0:
        vx = v0x + 1
    else:
        vx = 0
    vy = v0y - 1
    return x, y, vx, vy


def hit_area(vx, vy, tareax, tareay):
    x, y = 0, 0

    allx, ally = [0], [0]

    while True:
        x, y, vx, vy = shot_step(x, y, vx, vy)
        ally.append(y)
        allx.append(x)
        # print(x, y, vx, vy)
        if x >= tareax[0] and x <= tareax[1] and y >= tareay[0] and y <= tareay[1]:
            return True, allx, ally

        if vy < 0 and y < tareay[0]:
            return False, allx, ally


def max_vx0(maxx):
    return 0.5 * (np.sqrt(8 * maxx + 1) - 1)
    

    

if __name__ == '__main__':
    tareax = [20, 30]
    tareay = [-10, -5]

    for vx, vy in [(6, 9), (9, 0), (6, 3), (7, -1)]:
        print('*', vx, vy)
        test, xx, yy = hit_area(vx, vy, tareax, tareay)

        print(test)
        print(list(zip(xx, yy)))


    tareax, tareay = load_input()
    deltay = tareay[1] - tareay[0]
    deltax = tareax[1] - tareax[0]

    vxrange = [int(max_vx0(tareax[0])) + 1, tareax[1] + 1]
    print('v0x range:', vxrange)

    part1 = []
    part2 = 0

    for v0x in range(*vxrange):
        for v0y in range(tareay[0]-10, -tareay[0]+10):
            test, allx, ally = hit_area(v0x, v0y, tareax, tareay)
            if test:
                print(v0x, v0y, test)
                part2 += 1
                part1.extend(ally)

    print(max(part1))
    print(part2)