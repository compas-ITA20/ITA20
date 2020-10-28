import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas.utilities import i_to_rgb
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

TOL = 0.02
MAXDEV = 0.005
KMAX = 500

igl = Proxy('compas_libigl')

mesh = Mesh.from_off(compas.get('tubemesh.off'))

V, F = mesh.to_vertices_and_faces()
V2 = igl.quadmesh_planarize((V, F), KMAX, MAXDEV)

mesh = Mesh.from_vertices_and_faces(V2, F)

dev = mesh_flatness(mesh, maxdev=TOL)

artist = MeshArtist(mesh, layer="ITA20::Tubemesh")
artist.clear_layer()
artist.draw_faces(color={face: i_to_rgb(dev[face]) for face in mesh.faces()})
