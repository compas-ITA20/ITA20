import compas_rhino
from compas.geometry import add_vectors, subtract_vectors, length_vector
from compas.datastructures import Network
from compas_rhino.artists import NetworkArtist


def compute_residual(network, node):
    a = network.node_attributes(node, 'xyz')
    r = [0, 0, 0]
    for nbr in network.neighbors(node):
        b = network.node_attributes(nbr, 'xyz')
        edge = node, nbr
        if not network.has_edge(*edge):
            edge = nbr, node
        force = network.edge_attribute(edge, 'f')
        length = network.edge_length(*edge)
        r[0] += force * (b[0] - a[0]) / length
        r[1] += force * (b[1] - a[1]) / length
        r[2] += force * (b[2] - a[2]) / length
    return r


# clear the Rhino model

compas_rhino.clear()

# create a network

network = Network()

network.update_dna(is_anchor=False)
network.update_dna(rx=0, ry=0, rz=0)
network.update_dea(f=1)

a = network.add_node(x=0, y=0, z=0, is_anchor=True)
b = network.add_node(x=10, y=0, z=10, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e)
network.add_edge(b, e)
network.add_edge(c, e)
network.add_edge(d, e)

# move in the direction of the residual

for k in range(100):
    for node in network.nodes():
        r = compute_residual(network, node)
        network.node_attributes(node, ['rx', 'ry', 'rz'], r)

        if network.node_attribute(node, 'is_anchor'):
            continue

        rx, ry, rz = r
        x0, y0, z0 = network.node_attributes(node, 'xyz')
        x1 = x0 + 0.5 * rx
        y1 = y0 + 0.5 * ry
        z1 = z0 + 0.5 * rz
        network.node_attributes(node, 'xyz', [x1, y1, z1])

        r = compute_residual(network, node)
        network.node_attributes(node, ['rx', 'ry', 'rz'], r)

# visualize the geometry

layer = "ITA20::L5::FormFinding"

artist = NetworkArtist(network, layer=layer)

artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
artist.draw_edges()

# visualize the reaction forces

lines = []
for node in network.nodes_where({'is_anchor': True}):
    start = network.node_attributes(node, 'xyz')
    residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
    end = subtract_vectors(start, residual)
    color = (0, 255, 0)
    lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})

compas_rhino.draw_lines(lines, layer=layer)

# visualize the residual forces

lines = []
for node in network.nodes_where({'is_anchor': False}):
    start = network.node_attributes(node, 'xyz')
    residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
    if length_vector(residual) < 0.001:
        continue
    end = add_vectors(start, residual)
    color = (0, 255, 255)
    lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})

compas_rhino.draw_lines(lines, layer=layer)
