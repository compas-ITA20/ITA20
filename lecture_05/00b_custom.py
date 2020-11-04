import compas_rhino
from compas.datastructures import Network
from compas_rhino.artists import NetworkArtist

# clear the Rhino model

compas_rhino.clear()

# create a network

network = Network()

network.update_default_node_attributes(is_anchor=False)
network.update_default_node_attributes(rx=0, ry=0, rz=0)
network.update_default_edge_attributes(f=1)

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

artist = NetworkArtist(network)
artist.layer = "ITA20::L5::FormFinding"

node_color = {node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})}

artist.draw_nodes(color=node_color)
artist.draw_edges()
