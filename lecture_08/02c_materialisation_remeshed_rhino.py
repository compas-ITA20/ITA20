import os
from compas.datastructures import Mesh
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist

cgal = Proxy('compas_cgal.meshing')
# cgal.restart_server()

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'form_trimesh.json')
FILE_O = os.path.join(HERE, 'data', 'form_remeshed.json')

mesh = Mesh.from_json(FILE_I)

lengths = [mesh.edge_length(*edge) for edge in mesh.edges()]
length = sum(lengths) / mesh.number_of_edges()

V, F = cgal.remesh(mesh.to_vertices_and_faces(), 0.75 * length)
mesh = Mesh.from_vertices_and_faces(V, F)

mesh.to_json(FILE_O)

artist = MeshArtist(mesh, layer="RV2::Remeshed")
artist.clear_layer()
artist.draw_faces(join_faces=True)
