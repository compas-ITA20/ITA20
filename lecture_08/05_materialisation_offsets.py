import os

from compas.geometry import add_vectors, scale_vector
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'form_dual.json')

FILE_O1 = os.path.join(HERE, 'data', 'form_idos.json')
FILE_O2 = os.path.join(HERE, 'data', 'form_edos.json')

mesh = Mesh.from_json(FILE_I)

idos = mesh.copy()
edos = mesh.copy()

for vertex in mesh.vertices():
    point = mesh.vertex_coordinates(vertex)
    normal = mesh.vertex_normal(vertex)
    thickness = 0.10
    idos.vertex_attributes(vertex, 'xyz', add_vectors(point, scale_vector(normal, +0.5 * thickness)))
    edos.vertex_attributes(vertex, 'xyz', add_vectors(point, scale_vector(normal, -0.5 * thickness)))

idos.to_json(FILE_O1)
edos.to_json(FILE_O2)

artist = MeshArtist(None)

artist.mesh = idos
artist.layer = "RV2::Idos"
artist.clear_layer()
artist.draw_faces(color=(255, 0, 0))

artist.mesh = edos
artist.layer = "RV2::Edos"
artist.clear_layer()
artist.draw_faces(color=(0, 0, 255))
