import compas_blender
from compas.datastructures import Mesh
from compas_blender.artists import MeshArtist

compas_blender.clear()

mesh = Mesh.from_polyhedron(6)

artist = MeshArtist(mesh)
artist.draw()
