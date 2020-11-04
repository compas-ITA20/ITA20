import compas_rhino
from compas.datastructures import Network
from compas_rhino.artists import NetworkArtist

# clear the Rhino model

compas_rhino.clear()

# create a network

network = Network()

a = network.add_node(x=0, y=0, z=0)
b = network.add_node(x=10, y=0, z=10)
c = network.add_node(x=10, y=10, z=0)
d = network.add_node(x=0, y=10, z=10)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e)
network.add_edge(b, e)
network.add_edge(c, e)
network.add_edge(d, e)

# visualize the geometry

artist = NetworkArtist(network)

artist.layer = "ITA20::L5::FormFinding"
artist.draw()
