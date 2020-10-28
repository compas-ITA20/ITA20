import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

compas_rhino.clear()

mesh = Mesh.from_polyhedron(6)

artist = MeshArtist(mesh)
artist.draw()
