import os
import random
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.datastructures import Mesh

import compas_rhino
from __viz import CablenetArtist


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'hypar.json')

# load a mesh

mesh = Mesh.from_json(FILE)

# vertex neighbourhood

vertex = random.choice(list(set(mesh.vertices()) - set(mesh.vertices_on_boundary())))
nbrs = mesh.vertex_neighbors(vertex, ordered=True)

a = mesh.vertex_attributes(vertex, 'xyz')

lines = []
polygons = []
for nbr in nbrs:
    b = mesh.vertex_attributes(nbr, 'xyz')
    v0 = subtract_vectors(b, a)

    f1 = mesh.halfedge_face(vertex, nbr)
    c1 = mesh.face_centroid(f1)
    v1 = subtract_vectors(c1, a)

    f2 = mesh.halfedge_face(nbr, vertex)
    c2 = mesh.face_centroid(f2)
    v2 = subtract_vectors(c2, a)

    a1 = 0.25 * length_vector(cross_vectors(v0, v1))
    a2 = 0.25 * length_vector(cross_vectors(v0, v2))

    lines.append({'start': a, 'end': b, 'arrow': 'end', 'color': (0, 0, 255)})
    lines.append({'start': a, 'end': c1, 'arrow': 'end', 'color': (255, 0, 0)})

    polygons.append({'points': [a, b, add_vectors(b, v1), c1], 'color': (255, 0, 0)})
    polygons.append({'points': [a, b, add_vectors(b, v2), c2], 'color': (0, 0, 255)})


# visualize

artist = CablenetArtist(mesh, layer="ITA20::L5::FormFinding")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()

compas_rhino.draw_lines(lines, layer=artist.layer)
compas_rhino.draw_faces(polygons, layer=artist.layer)
