import compas
import compas_rhino
from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas_rhino.artists import MeshArtist

numerical = Proxy('compas.numerical')
fd_numpy = numerical.fd_numpy

compas_rhino.clear()

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.update_default_vertex_attributes(is_anchor=False)
mesh.update_default_vertex_attributes(px=0.0, py=0.0, pz=0.0)
mesh.update_default_vertex_attributes(rx=0.0, ry=0.0, rz=0.0)

mesh.update_default_edge_attributes(q=1.0, f=0.0, l=0.0)

corners = list(mesh.vertices_where({'vertex_degree': 2}))
mesh.vertices_attribute('is_anchor', True, keys=corners)
mesh.vertices_attribute('z', 7.0, keys=[0, 35])
mesh.edges_attribute('q', 10, keys=list(mesh.edges_on_boundary()))

key_index = mesh.key_index()
xyz = mesh.vertices_attributes('xyz')
loads = mesh.vertices_attributes(('px', 'py', 'pz'))
fixed = [key_index[key] for key in mesh.vertices_where({'is_anchor': True})]
edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
q = mesh.edges_attribute('q')

xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

for key, attr in mesh.vertices(True):
    index = key_index[key]
    mesh.vertex_attributes(key, 'xyz', xyz[index])
    mesh.vertex_attributes(key, ['rx', 'ry', 'rz'], r[index])

for index, (key, attr) in enumerate(mesh.edges(True)):
    attr['q'] = q[index][0]
    attr['f'] = f[index][0]
    attr['l'] = l[index][0]

artist = MeshArtist(mesh)
artist.draw_mesh()
