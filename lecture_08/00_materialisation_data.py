import os
import compas

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'sessions', 'bm_vertical_equilibrium', 'bm_a_06_vertical.rv2')
FILE_O = os.path.join(HERE, 'data', 'form.json')

session = compas.json_load(FILE_I)

form = Mesh.from_data(session['data']['form'])
form.to_json(FILE_O)

artist = MeshArtist(form, layer="RV2::Mesh")
artist.clear_layer()
artist.draw_faces(join_faces=True)
