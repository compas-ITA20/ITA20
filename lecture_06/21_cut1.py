# identify block sides
# and synchronize vertex order

import os

from compas.datastructures import Mesh
from compas.geometry import Polygon, Line
from compas.geometry import dot_vectors, distance_point_point

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist, MeshArtist, BoxArtist

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
# Left/Right
# ==============================================================================

left = sorted(block.faces(), key=lambda face: dot_vectors(block.face_normal(face), [-1, 0, 0]))[-1]
right = sorted(block.faces(), key=lambda face: dot_vectors(block.face_normal(face), [+1, 0, 0]))[-1]

# left vertices

left_vertices = block.face_vertices(left)
left_points = block.vertices_attributes('xyz', keys=left_vertices)

# sorted left vertices starting at bottom left

point = blank.points[0]
distances = [distance_point_point(p, point) for p in left_points]

vertex = sorted(zip(left_vertices, distances), key=lambda x: x[1])[0][0]
i = left_vertices.index(vertex)

left_vertices = left_vertices[i:] + left_vertices[:i]
left_points = block.vertices_attributes('xyz', keys=left_vertices)

# corresponding right vertices

right_vertices = block.face_vertices(right)[::-1]

i = None
for nbr in block.vertex_neighbors(left_vertices[0]):
    if nbr not in left_vertices:
        i = right_vertices.index(nbr)
        break

right_vertices = right_vertices[i:] + right_vertices[:i]
right_points = block.vertices_attributes('xyz', keys=right_vertices)

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

line = Line([0, 0, 0], [WIRE, 0, 0])
artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::Wire")
artist.draw()

# block and blank

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces(color={left: (255, 0, 0), right: (0, 255, 0)}, faces=[left, right])

text = {}
text.update({vertex: str(i) for i, vertex in enumerate(left_vertices)})
text.update({vertex: str(i) for i, vertex in enumerate(right_vertices)})

color = {}
color.update({vertex: (255, 0, 0) for vertex in left_vertices})
color.update({vertex: (0, 255, 0) for vertex in right_vertices})

artist.draw_vertexlabels(text=text, color=color)

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)

for a, b in zip(left_points, right_points):
    line = Line(a, b)
    artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::CutLines")
    artist.draw()
