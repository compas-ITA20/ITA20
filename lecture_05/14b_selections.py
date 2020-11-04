import compas
from compas.datastructures import Mesh
from compas.rpc import Proxy

import compas_rhino
from __viz import CablenetArtist


proxy = Proxy('compas.numerical')
fd = proxy.fd_numpy

# make a mesh

mesh = Mesh.from_obj(compas.get('hypar.obj'))

# set boundary conditions

mesh.update_default_vertex_attributes(is_anchor=False)
mesh.update_default_vertex_attributes(px=0, py=0, pz=0)
mesh.update_default_vertex_attributes(rx=0, ry=0, rz=0)
mesh.update_default_edge_attributes(q=1.0, f=0.0)

corners = list(mesh.vertices_where({'vertex_degree': 2}))

for vertex in corners:
    mesh.vertex_attribute(vertex, 'is_anchor', True)

for edge in mesh.edges_on_boundary():
    mesh.edge_attribute(edge, 'q', 5.0)

# compile numerical data

vertex_index = mesh.vertex_index()

X = mesh.vertices_attributes('xyz')
P = mesh.vertices_attributes(['px', 'py', 'pz'])
Q = mesh.edges_attribute('q')

fixed = [vertex_index[vertex] for vertex in mesh.vertices_where({'is_anchor': True})]
E = [(vertex_index[u], vertex_index[v]) for u, v in mesh.edges()]

# compute equilibrium

X, Q, F, L, R = fd(X, E, fixed, Q, P)

# update network

for vertex in mesh.vertices():
    index = vertex_index[vertex]
    mesh.vertex_attributes(vertex, 'xyz', X[index])

# visualize the initial state

artist = CablenetArtist(mesh, layer="ITA20::L5::FormFinding")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
guids = artist.draw_edges()
artist.redraw()

guid_edge = dict(zip(guids, mesh.edges()))
edge_index = {edge: index for index, edge in enumerate(mesh.edges())}

# modify force densities of selected edges

while True:
    guids = compas_rhino.select_lines()
    if not guids:
        break

    guid = guids[0]
    if guid in guid_edge:
        edge = guid_edge[guid]
        edges = mesh.edge_loop(edge)
        for edge in edges:
            index = edge_index[edge]
            Q[index][0] *= 2

        # update equilibrium

        X, Q, F, L, R = fd(X, E, fixed, Q, P)

        # update network

        for vertex in mesh.vertices():
            index = vertex_index[vertex]
            mesh.vertex_attributes(vertex, 'xyz', X[index])

        # update visualization

        artist.clear_layer()
        artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
        guids = artist.draw_edges()
        artist.redraw()

        guid_edge = dict(zip(guids, mesh.edges()))

# update network

for vertex in mesh.vertices():
    index = vertex_index[vertex]
    mesh.vertex_attributes(vertex, 'xyz', X[index])
    mesh.vertex_attributes(vertex, ['rx', 'ry', 'rz'], R[index])

for index, edge in enumerate(mesh.edges()):
    mesh.edge_attribute(edge, 'q', Q[index][0])
    mesh.edge_attribute(edge, 'f', F[index][0])

# visualize result

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()
artist.draw_residuals()
artist.draw_reactions()
artist.draw_forces(scale=0.01)
