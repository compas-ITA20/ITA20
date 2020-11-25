from compas.geometry import Bezier
from compas.geometry import Point, Vector, Line, Polyline, Frame
from compas.geometry import offset_polyline
from compas.geometry import intersection_line_segment_xy
from compas.utilities import linspace, pairwise, window

from compas_plotters import GeometryPlotter


def intersection_line_polyline(line, polyline):
    for segment in pairwise(polyline.points):
        x = intersection_line_segment_xy(line, segment)
        if x:
            return Point(*x)


controlpoints = [Point(0, 0, 0), Point(4, 2.5, 0), Point(6, -2.5, 0), Point(10, 0, 0)]
controlpoly = Polyline(controlpoints)

curve = Bezier(controlpoints)
poly = Polyline(curve.locus())
poly1 = Polyline(offset_polyline(poly, +0.15))
poly2 = Polyline(offset_polyline(poly, -0.15))

points = [poly.point(t) for t in linspace(0, 1, 20)]
tangents = [(c - a).unitized() for a, b, c in window(points, 3) if a and c]
normals = [Vector(0, 0, 1).cross(t) for t in tangents]
lines = [[point, point + normal] for point, normal in zip(points[1:-1], normals)]

points1 = [intersection_line_polyline(line, poly1) for line in lines]
points2 = [intersection_line_polyline(line, poly2) for line in lines]

frames = []
for a, b in pairwise(points[1:-1]):
    p = (a + b) * 0.5
    t = (b - a).unitized()
    n = Vector(0, 0, 1).cross(t)
    frame = Frame(p, t, n)
    frames.append(frame)

# ==============================================================================
# Visualization
# ==============================================================================

plotter = GeometryPlotter(figsize=(16, 9))

plotter.add(controlpoly, linestyle='dotted', linewidth=0.5, color=(0.5, 0.5, 0.5))
for point in controlpoints:
    plotter.add(point, edgecolor=(1.0, 0.0, 0.0))

plotter.add(poly, color=(0.4, 0.4, 0.4))
plotter.add(poly1, color=(0.0, 0.0, 0.0))
plotter.add(poly2, color=(0.0, 0.0, 0.0))

for point in points:
    plotter.add(point, size=2)

for point in points1:
    plotter.add(point, size=2)

for point in points2:
    plotter.add(point, size=2)

for point, normal in zip(points[1:-1], normals):
    a = point + normal
    b = point - normal
    line = Line(a, b)
    plotter.add(line, color=(0.5, 0.5, 0.5), draw_as_segment=True, linestyle='dashed', linewidth=0.5)

for frame in frames:
    point = frame.point
    xaxis = Line(point, point + frame.xaxis * 0.1)
    yaxis = Line(point, point + frame.yaxis * 0.1)
    plotter.add(point, edgecolor=(0, 0, 1.0), size=2)
    plotter.add(xaxis, color=(1.0, 0, 0), draw_as_segment=True)
    plotter.add(yaxis, color=(0, 1.0, 0), draw_as_segment=True)

plotter.zoom_extents()
plotter.show()
