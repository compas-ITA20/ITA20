# block and blank wrt to the cutting tool

import os

from compas.datastructures import Mesh
from compas.geometry import Polygon, Line

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist, MeshArtist, BoxArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'block.json')

# ==============================================================================
# Parameters
# ==============================================================================

WIRE = 1600
TABLE = 1500
HEIGHT = 1000

# ==============================================================================
# Block and Blank
# ==============================================================================

block = Mesh.from_json(FILE_I)
blank = block.attributes['blank']

# ==============================================================================
# Visualize
# ==============================================================================

compas_rhino.clear()

# cutter

points = [[0, 0, 0], [0, 0, HEIGHT], [0, TABLE, HEIGHT], [0, TABLE, 0]]
polygon = Polygon(points)

artist = PolygonArtist(polygon, layer="ITA20::HotWire::Left", color=(255, 0, 0))
artist.draw(show_edges=True, show_face=False)

points = [[WIRE, 0, 0], [WIRE, 0, HEIGHT], [WIRE, TABLE, HEIGHT], [WIRE, TABLE, 0]]
polygon = Polygon(points)

artist = PolygonArtist(polygon, layer="ITA20::Hotwire::Right", color=(0, 255, 0))
artist.draw(show_edges=True, show_face=False)

line = Line([0, 0, 0], [WIRE, 0, 0])

artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::Wire")
artist.draw()

# block and blank

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces()

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)
