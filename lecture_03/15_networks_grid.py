from itertools import combinations

from compas.datastructures import Network
from compas.utilities import linspace, meshgrid
from compas_rhino.artists import NetworkArtist

X, Y = meshgrid(linspace(0, 10, 10), linspace(0, 5, 5))

points = []
for z in linspace(0, 3, 3):
    for xs, ys in zip(X, Y):
        for x, y in zip(xs, ys):
            points.append([x, y, z])

network = Network()

for point in points:
    network.add_node(x=point[0], y=point[1], z=point[2])

for a, b in combinations(network.nodes(), 2):
    if network.node_attribute(a, 'z') != network.node_attribute(b, 'z'):
        network.add_edge(a, b)

artist = NetworkArtist(network, layer="ITA20::Network")
artist.clear_layer()
artist.draw_nodes()
artist.draw_edges()
