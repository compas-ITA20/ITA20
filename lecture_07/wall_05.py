from compas.geometry import Bezier
from compas.geometry import Point, Vector, Line, Polyline
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

plotter.zoom_extents()
plotter.show()
