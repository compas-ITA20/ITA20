# define cutting tool

from compas.geometry import Polygon, Line

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist

# ==============================================================================
# Parameters
# ==============================================================================

WIRE = 1600
TABLE = 1500
HEIGHT = 1000

# ==============================================================================
# Visualize
# ==============================================================================

compas_rhino.clear()

# draw movement boundaries left

points = [
    [0, 0, 0],
    [0, 0, HEIGHT],
    [0, TABLE, HEIGHT],
    [0, TABLE, 0]
]
polygon = Polygon(points)

artist = PolygonArtist(polygon, layer="ITA20::HotWire::Left", color=(255, 0, 0))
artist.draw(show_edges=True, show_face=False)

# draw movement boundaries right

points = [
    [WIRE, 0, 0],
    [WIRE, 0, HEIGHT],
    [WIRE, TABLE, HEIGHT],
    [WIRE, TABLE, 0]
]
polygon = Polygon(points)

artist = PolygonArtist(polygon, layer="ITA20::Hotwire::Right", color=(0, 255, 0))
artist.draw(show_edges=True, show_face=False)

# draw the wire

line = Line([0, 0, 0], [WIRE, 0, 0])

artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::Wire")
artist.draw()
