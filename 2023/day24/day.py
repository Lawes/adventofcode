import pycommon as M
import itertools
import numpy as np
import scipy


def intersect(ha, hb):
    xa, ya, za, vxa, vya, vza = ha
    xb, yb, zb, vxb, vyb, vzb = hb

    det = (vxa * vyb) - (vya * vxb)

    if det == 0:
        return None

    t1 = - (xa - xb) * vyb + (ya - yb) * vxb
    t1 /= det

    xi = xa + t1 * vxa
    yi = ya + t1 * vya

    t2 = - (xa - xb) * vya + (ya - yb) * vxa
    t2 /= det

    return (xi, yi, t1, t2)


@M.timeperf
def test():
    M.log()
    data = M.ints_file('input_test')

    for h1, h2 in itertools.combinations(data, r=2):
        print(h1, h2)
        pt = intersect(h1, h2)
        print(pt)
        if pt is not None:
            if 7 <= pt[0] <= 27 and 7 <= pt[1] <= 27 and pt[2] > 0 and pt[3] > 0:
                print('intersect')


@M.timeperf
def part1():
    data = M.ints_file('input')

    total = 0
    for i1, h1 in enumerate(data):
        for h2 in data[:i1]:
            pt = intersect(h1, h2)
            if pt is not None:
                if 200000000000000 <= pt[0] <= 400000000000000 and 200000000000000 <= pt[1] <= 400000000000000 and pt[2] > 0 and pt[3] > 0:
                    total += 1
    print('part1', total)


def array_data(data):
    elem = list(zip(*data))
    return [np.array(e) for e in elem]



def func(v, *args):
    x, y, z, vx, vy, vz = v
    xa, ya, za, vxa, vya, vza = args

    r1 = (x - xa) * (vya - vy) + (y - ya) * (vx - vxa)
    r2 = (y - ya) * (vza - vz) + (z - za) * (vy - vya)

    return np.dot(r1, r1) + np.dot(r2, r2)





@M.timeperf
def part2():
    # ça marche pas pour input, mais ok pour input_test
    data = M.ints_file('input')

    xa, ya, za, vxa, vya, vza = array_data(data)

    print(func([24, 13, 10, -3, 1, 2], xa, ya, za, vxa, vya, vza))

    res = scipy.optimize.minimize(
        func,
        #bounds=[(0, 400000000000000), (0, 400000000000000), (0, 400000000000000), (-500, 500),  (-500, 500),  (-500, 500)],
        x0=[0, 0, 0, 0, 0, 0], args=(xa, ya, za, vxa, vya, vza), tol=0.1)
    print(res)
    res = [int(v + 0.5) for v in res.x]

    print('part2', res[0] + res[1] + res[2])


if __name__ == '__main__':
    test()
    part1()
    part2()