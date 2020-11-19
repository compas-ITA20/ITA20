# position block for cut 1

import os

from compas.datastructures import Mesh
from compas.geometry import Polygon, Line, Point
from compas.geometry import Translation

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist, MeshArtist, BoxArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'block.json')
FILE_O = os.path.join(HERE, 'data', 'block_cut1.json')

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
# Transform to table zero for cut 1
# ==============================================================================

p0 = blank.points[0]
p1 = blank.points[3]
v = p1 - p0

a = p0 + v * 0.5
b = Point(0.5 * TABLE, 0, 0)

T = Translation.from_vector(b - a)

block.transform(T)
blank.transform(T)

# ==============================================================================
# Export
# ==============================================================================

block.to_json(FILE_O)

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

artist = PolygonArtist(polygon, layer="ITA20::HotWire::Right", color=(0, 255, 0))
artist.draw(show_edges=True, show_face=False)

line = Line([0, 0, 0], [WIRE, 0, 0])

artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::Wire")
artist.draw()

# blank and block

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces()

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)
