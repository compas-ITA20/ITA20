from __future__ import print_function

from compas.rpc import Proxy

proxy = Proxy()

A = [[3, 2, 0], [1, -1, 0], [0, 5, 1]]
b = [2, 4, -1]

proxy.package = "scipy.linalg"
x = proxy.solve(A, b)

print(x)
