# left/right
# movement paths
# store cutting data

import os

from compas.datastructures import Mesh
from compas.geometry import Polygon, Line, Plane, Polyline
from compas.geometry import dot_vectors, distance_point_point, intersection_line_plane

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist, MeshArtist, BoxArtist, PolylineArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'block_cut2.json')
FILE_O = os.path.join(HERE, 'data', 'block_cut2.json')

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

right_vertices = right_vertices[i:] + right_vertices[:i]
right_points = block.vertices_attributes('xyz', keys=right_vertices)

# ==============================================================================
# Movement paths
# ==============================================================================

left_plane = Plane([0, 0, 0], [-1, 0, 0])
right_plane = Plane([WIRE, 0, 0], [+1, 0, 0])

left_intersections = [left_plane.point]
right_intersections = [right_plane.point]

for line in zip(left_points, right_points):
    left_x = intersection_line_plane(line, left_plane)
    right_x = intersection_line_plane(line, right_plane)

    left_intersections.append(left_x)
    right_intersections.append(right_x)

left_intersections.append(left_intersections[1])
right_intersections.append(right_intersections[1])

left_intersections.append(left_intersections[0])
right_intersections.append(right_intersections[0])

# polylines

left_poly = Polyline(left_intersections)
right_poly = Polyline(right_intersections)

block.attributes['sides'] = {'left': left, 'right': right}
block.attributes['cut1'] = {'left': left_poly, 'right': right_poly}

# ==============================================================================
# Export
# ==============================================================================

block.to_json(FILE_O)

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
