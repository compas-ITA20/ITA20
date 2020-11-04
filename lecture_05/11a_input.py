import compas_rhino
from compas.geometry import length_vector, add_vectors, subtract_vectors
from compas.geometry import Cylinder
from compas.datastructures import Network
from compas.numerical import dr
from compas.utilities import geometric_key
from compas_rhino.artists import NetworkArtist
from compas_rhino.artists import CylinderArtist


class CablenetArtist(NetworkArtist):

    def draw_reactions(self, color=(0, 255, 0)):
        lines = []
        for node in self.network.nodes_where({'is_anchor': True}):
            start = self.network.node_attributes(node, 'xyz')
            residual = self.network.node_attributes(node, ['rx', 'ry', 'rz'])
            end = subtract_vectors(start, residual)
            lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})
        compas_rhino.draw_lines(lines, layer=self.layer)

    def draw_residuals(self, color=(0, 255, 255), tol=0.01):
        lines = []
        for node in self.network.nodes_where({'is_anchor': False}):
            start = self.network.node_attributes(node, 'xyz')
            residual = self.network.node_attributes(node, ['rx', 'ry', 'rz'])
            if length_vector(residual) < tol:
                continue
            end = add_vectors(start, residual)
            lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})
        compas_rhino.draw_lines(lines, layer=self.layer)

    def draw_forces(self, color=(255, 0, 0), scale=0.1, tol=0.001):
        for edge in self.network.edges():
            f = self.network.edge_attribute(edge, 'f')
            l = self.network.edge_length(*edge)  # noqa E741
            radius = scale * f
            if radius < tol:
                continue
            mp = self.network.edge_midpoint(*edge)
            direction = self.network.edge_direction(*edge)
            cylinder = Cylinder(((mp, direction), radius), l)
            artist = CylinderArtist(cylinder, layer=self.layer, color=color)
            artist.draw(u=16)


def update_network():
    for node in network.nodes():
        index = node_index[node]
        network.node_attributes(node, 'xyz', X[index])
        network.node_attributes(node, ['rx', 'ry', 'rz'], R[index])

    for index, edge in enumerate(network.edges()):
        network.edge_attribute(edge, 'q', Q[index])
        network.edge_attribute(edge, 'f', F[index])


def callback(k, X, crits, args):
    for node in network.nodes():
        index = node_index[node]
        network.node_attributes(node, 'xyz', X[index])

    artist.clear_layer()
    artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
    artist.draw_edges()
    compas_rhino.rs.Redraw()
    compas_rhino.wait()


# clear the Rhino model

# compas_rhino.clear()

# create a network

guids = compas_rhino.select_lines()
lines = compas_rhino.get_line_coordinates(guids)

guids = compas_rhino.select_points()
points = compas_rhino.get_point_coordinates(guids)

network = Network.from_lines(lines)

network.update_dna(is_anchor=False)
network.update_dna(rx=0, ry=0, rz=0)
network.update_dna(px=0, py=0, pz=0)
network.update_dea(q=1)

gkey_node = network.gkey_key()
for point in points:
    gkey = geometric_key(point)
    if gkey in gkey_node:
        node = gkey_node[gkey]
        network.node_attribute(node, 'is_anchor', True)

# numerical data

node_index = {node: index for index, node in enumerate(network.nodes())}

fixed = list(network.nodes_where({'is_anchor': True}))
free = list(network.nodes_where({'is_anchor': False}))
fixed[:] = [node_index[node] for node in fixed]
free[:] = [node_index[node] for node in free]

edges = [(node_index[u], node_index[v]) for u, v in network.edges()]

X = network.nodes_attributes('xyz')
R = network.nodes_attributes(['rx', 'ry', 'rz'])
P = network.nodes_attributes(['px', 'py', 'pz'])
Q = network.edges_attribute('q')

# create an artist
# the artist has to be created before passing the callback to the DR algorithm

artist = CablenetArtist(network, layer="ITA20::L5::FormFinding")

# compute equilibrium

X, Q, F, L, R = dr(X, edges, fixed, P, Q, callback=callback)

# update network

update_network()

# visualize result

artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
artist.clear_layer()

artist.draw_edges()
artist.draw_residuals()
artist.draw_reactions()
artist.draw_forces(scale=0.05)
