from compas.geometry import Bezier
from compas.geometry import Point, Vector, Line, Frame, Polyline, Box, Polygon
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
normals = [vector.cross([0, 0, 1]) for vector in tangents]
lines = [[point, point + normal] for point, normal in zip(points[1:-1], normals)]

points1 = [intersection_line_polyline(line, poly1) for line in lines]
points2 = [intersection_line_polyline(line, poly2) for line in lines]

frames = []
blocks = []

for (a, b), (a1, b1), (a2, b2) in zip(pairwise(points[1:-1]), pairwise(points1), pairwise(points2)):
    p = (a + b) * 0.5
    t = (b - a).unitized()
    n = Vector(0, 0, 1).cross(t)

    frame = Frame(p, t, n)
    frames.append(frame)

    l1 = (b1 - a1).length
    l2 = (b2 - a2).length

    block = Box(frame, min(l1, l2) - 0.03, 0.3, 0.1)
    blocks.append(Polygon(block.vertices[:4][::-1]))

# ==============================================================================
# Visualization
# ==============================================================================

plotter = GeometryPlotter(figsize=(16, 9))

plotter.add(controlpoly, linestyle='dotted', linewidth=0.5, color=(0.5, 0.5, 0.5))
for point in controlpoints:
    plotter.add(point, edgecolor=(1.0, 0.0, 0.0))

plotter.add(poly, color=(0.7, 0.7, 0.7), linewidth=0.5)
plotter.add(poly1, color=(0.7, 0.7, 0.7), linewidth=0.5)
plotter.add(poly2, color=(0.7, 0.7, 0.7), linewidth=0.5)

for frame in frames:
    point = frame.point
    xaxis = Line(point, point + frame.xaxis * 0.1)
    yaxis = Line(point, point + frame.yaxis * 0.1)
    plotter.add(point, edgecolor=(0, 0, 1.0), size=2)
    plotter.add(xaxis, color=(1.0, 0, 0), draw_as_segment=True)
    plotter.add(yaxis, color=(0, 1.0, 0), draw_as_segment=True)

for block in blocks:
    plotter.add(block)

plotter.zoom_extents()
plotter.show()
