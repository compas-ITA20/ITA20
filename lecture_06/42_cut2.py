import os
import math

from compas.datastructures import Mesh
from compas.geometry import Polygon, Line, Point, Plane, Polyline
from compas.geometry import dot_vectors, distance_point_point, intersection_line_plane
from compas.geometry import Rotation, Translation
from compas.utilities import pairwise, linspace

import compas_rhino
from compas_rhino.artists import PolygonArtist, LineArtist, MeshArtist, BoxArtist, PolylineArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'block.json')
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
# Transform to table zero for cut 2
# ==============================================================================

Rz = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
Ry = Rotation.from_axis_and_angle([0, 1, 0], math.radians(90))

R = Ry * Rz

block.transform(R)
blank.transform(R)

p0 = blank.points[0]
p1 = blank.points[4]

v = p1 - p0

a = p0 + v * 0.5
b = Point(0.5 * TABLE, 0, 0)

T = Translation.from_vector(b - a)

block.transform(T)
blank.transform(T)

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
# Blank polylines
# ==============================================================================

left_plane = Plane(blank.points[0], [-1, 0, 0])
right_plane = Plane(blank.points[4], [+1, 0, 0])

left_blank = []
right_blank = []

for line in zip(left_poly.points, right_poly.points):
    left_x = intersection_line_plane(line, left_plane)
    right_x = intersection_line_plane(line, right_plane)

    left_blank.append(left_x)
    right_blank.append(right_x)

# ==============================================================================
# Visualization
# ==============================================================================

compas_rhino.clear()

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces(color={left: (255, 0, 0), right: (0, 255, 0)})

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)

points = [[0, 0, 0], [0, 0, HEIGHT], [0, TABLE, HEIGHT], [0, TABLE, 0]]
polygon = Polygon(points)
artist = PolygonArtist(polygon, layer="ITA20::HotWire::Left", color=(255, 0, 0))
artist.draw(show_edges=True, show_face=False)

points = [[WIRE, 0, 0], [WIRE, 0, HEIGHT], [WIRE, TABLE, HEIGHT], [WIRE, TABLE, 0]]
polygon = Polygon(points)
artist = PolygonArtist(polygon, layer="ITA20::HotWire::Right", color=(0, 255, 0))
artist.draw(show_edges=True, show_face=False)

artist = PolylineArtist(left_poly, color=(255, 0, 0), layer="ITA20::HotWire::LeftCut")
artist.draw()

artist = PolylineArtist(right_poly, color=(0, 255, 0), layer="ITA20::HotWire::RightCut")
artist.draw()

compas_rhino.rs.Redraw()

for i, j in pairwise(range(len(left_poly.points))):
    left_start = left_poly.points[i]
    left_stop = left_poly.points[j]
    left_vector = left_stop - left_start

    right_start = right_poly.points[i]
    right_stop = right_poly.points[j]
    right_vector = right_stop - right_start

    for n in linspace(0, 1, 50):
        a = left_start + left_vector * n
        b = right_start + right_vector * n
        line = Line(a, b)
        artist = LineArtist(line, color=(255, 255, 255), layer="ITA20::HotWire::CutLines")
        artist.clear_layer()
        artist.draw()
        compas_rhino.rs.Redraw()
        compas_rhino.wait()

    a = left_blank[i]
    b = right_blank[i]
    c = right_blank[j]
    d = left_blank[j]

    polygon = Polygon([a, b, c, d])
    artist = PolygonArtist(polygon, color=(255, 255, 255), layer="ITA20::HotWire::CutPlane")
    artist.draw()
