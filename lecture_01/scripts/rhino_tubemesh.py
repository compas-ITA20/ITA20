import compas
from compas.datastructures import Mesh

import compas_rhino
from compas_rhino.artists import MeshArtist

mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

artist = MeshArtist(mesh)
artist.draw_mesh()
