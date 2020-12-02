import os
import bpy

from compas.datastructures import Mesh
from compas_cgal.meshing import remesh

import compas_blender
from compas_blender.artists import MeshArtist

HERE = os.path.dirname(bpy.context.space_data.text.filepath)
FILE_I = os.path.join(HERE, 'data', 'form_trimesh.json')
FILE_O = os.path.join(HERE, 'data', 'form_remeshed.json')

compas_blender.clear()

mesh = Mesh.from_json(FILE_I)

lengths = [mesh.edge_length(*edge) for edge in mesh.edges()]
length = sum(lengths) / mesh.number_of_edges()

V, F = remesh(mesh.to_vertices_and_faces(), 0.75 * length)
mesh = Mesh.from_vertices_and_faces(V, F)

mesh.to_json(FILE_O)

artist = MeshArtist(mesh)
artist.draw_faces()
