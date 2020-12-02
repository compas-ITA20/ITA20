import os
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'form_remeshed.json')
FILE_O = os.path.join(HERE, 'data', 'form_dual.json')

mesh = Mesh.from_json(FILE_I)
dual = mesh.dual()

dual.to_json(FILE_O)

artist = MeshArtist(dual, layer="RV2::Dual")
artist.clear_layer()
artist.draw_faces()
