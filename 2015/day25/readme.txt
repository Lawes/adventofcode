e(row, column) = (row + column - 1)*(row + column - 2) / 2 + k - 1

ressultat = (power_modulo(252533, e(row, column), 33554393) * 20151125) % 33554393

In [5]: (pow(252533, 18168397-1, 33554393) * 20151125) % 33554393
Out[5]: 8997277
