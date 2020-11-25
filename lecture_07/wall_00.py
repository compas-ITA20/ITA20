from compas.geometry import Bezier
from compas.geometry import Point, Polyline

from compas_plotters import GeometryPlotter


controlpoints = [Point(0, 0, 0), Point(4, 2.5, 0), Point(6, -2.5, 0), Point(10, 0, 0)]

curve = Bezier(controlpoints)
poly = Polyline(curve.locus())
controlpoly = Polyline(controlpoints)

# ==============================================================================
# Visualization
# ==============================================================================

plotter = GeometryPlotter(figsize=(16, 9))

for point in controlpoints:
    plotter.add(point, edgecolor=(1.0, 0.0, 0.0))

plotter.add(controlpoly, linestyle='dotted', linewidth=1.0, color=(0.5, 0.5, 0.5))
plotter.add(poly, color=(0.4, 0.4, 0.4))

plotter.zoom_extents()
plotter.show()
