from __future__ import print_function

from compas.rpc import Proxy

linalg = Proxy("scipy.linalg")

A = [[3, 2, 0], [1, -1, 0], [0, 5, 1]]
b = [2, 4, -1]

x = linalg.solve(A, b)

print(x)
