import os

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'form_remeshed.json')

mesh = Mesh.from_json(FILE_I)

artist = MeshArtist(mesh, layer="RV2::Remeshed")
artist.clear_layer()
artist.draw_faces(join_faces=True)
