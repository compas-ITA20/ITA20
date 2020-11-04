import compas_rhino
from compas.geometry import subtract_vectors
from compas.geometry import normalize_vector
from compas.geometry import Cylinder, Cone
from compas.geometry import Frame, Scale, Transformation
from compas.datastructures import Network
from compas_rhino.artists import NetworkArtist
from compas_rhino.artists import CylinderArtist, ConeArtist

# clear the Rhino model

compas_rhino.clear()

# create a network
# with 5 nodes and 4 edges

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

# visualize the geometry

layer = "ITA20::L5::FormFinding"
artist = NetworkArtist(network, layer=layer)

node_color = {node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})}

artist.draw_nodes(color=node_color)
artist.draw_edges()

# visualize the forces

height = 1.0
world = Frame.worldXY()

circle = [[0, 0, 0.5 * 0.7 * height], [0, 0, 1]], 0.05
cylinder = Cylinder(circle, 0.7 * height)

circle = [[0, 0, 0.7 * height], [0, 0, 1]], 0.1
cone = Cone(circle, 0.3 * height)

for node in network.nodes():
    a = network.node_attributes(node, 'xyz')

    for nbr in network.neighbors(node):
        edge = node, nbr
        if not network.has_edge(*edge):
            edge = nbr, node

        b = network.node_attributes(nbr, 'xyz')
        force = network.edge_attribute(edge, 'f')
        direction = normalize_vector(subtract_vectors(b, a))

        frame = Frame.from_plane([a, direction])
        X = Transformation.from_frame_to_frame(world, frame)
        S = Scale.from_factors([force, 1, 1])
        X = X * S

        shaft = cylinder.transformed(X)
        tip = cone.transformed(X)

        artist = CylinderArtist(shaft, layer=layer, color=(255, 0, 0))
        artist.draw(u=16)

        artist = ConeArtist(tip, layer=layer, color=(255, 0, 0))
        artist.draw(u=16)
