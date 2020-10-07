from random import uniform
from compas.geometry import Circle
from compas_plotters.geometryplotter import GeometryPlotter


def pointcloud(N, xlim, ylim):
    xmin, xmax = xlim
    ymin, ymax = ylim
    x = [uniform(xmin, xmax) for i in range(N)]
    y = [uniform(ymin, ymax) for i in range(N)]
    z = [0.0] * N
    return list(zip(x, y, z))


xlim = (0, 8)
ylim = (0, 5)
cloud = pointcloud(30, xlim, ylim)

plotter = GeometryPlotter(show_axes=False)

for point in cloud:
    plane = [point, [0, 0, 1]]
    radius = 0.1
    plotter.add(Circle(plane, radius))

plotter.show()
