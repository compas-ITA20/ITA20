import compas
from compas.datastructures import Mesh

import compas_blender
from compas_blender.artists import MeshArtist

compas_blender.clear()

mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

artist = MeshArtist(mesh)
artist.draw_mesh()
