# process visualization 3

import os

from compas.datastructures import Mesh
from compas.geometry import Polygon, Line
from compas.utilities import linspace, pairwise

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist, MeshArtist, BoxArtist, PolylineArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'block_cut1.json')

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
# Cut data
# ==============================================================================

left = block.attributes['sides']['left']
right = block.attributes['sides']['right']

left_poly = block.attributes['cut1']['left']
right_poly = block.attributes['cut1']['right']

# ==============================================================================
# Visualization
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

# blank and block

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces(color={left: (255, 0, 0), right: (0, 255, 0)})

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)

# movement paths

artist = PolylineArtist(left_poly, color=(255, 0, 0), layer="ITA20::HotWire::LeftCut")
artist.draw()

artist = PolylineArtist(right_poly, color=(0, 255, 0), layer="ITA20::HotWire::RightCut")
artist.draw()

# cutting process

compas_rhino.rs.Redraw()

for i, j in pairwise(range(len(left_poly.points))):
    left_start = left_poly.points[i]
    left_stop = left_poly.points[j]
    left_vector = left_stop - left_start

    right_start = right_poly.points[i]
    right_stop = right_poly.points[j]
    right_vector = right_stop - right_start

    for i in linspace(0, 1, 50):
        a = left_start + left_vector * i
        b = right_start + right_vector * i
        line = Line(a, b)
        artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::CutLines")
        artist.clear_layer()
        artist.draw()
        compas_rhino.rs.Redraw()
        compas_rhino.wait()

    polygon = Polygon([left_start, right_start, right_stop, left_stop])
    artist = PolygonArtist(polygon, color=(255, 255, 255), layer="ITA20::HotWire::CutPlane")
    artist.draw()
