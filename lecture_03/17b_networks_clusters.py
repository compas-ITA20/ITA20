import os

from compas.datastructures import Network
from compas.utilities import i_to_rgb
from compas_rhino.artists import NetworkArtist


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'clusters.json')

network = Network.from_json(FILE)

artist = NetworkArtist(network, layer="ITA20::Network")
artist.clear_layer()

nodecolor = {node: i_to_rgb(network.node_attribute(node, 'cluster') / 9) for node in network.nodes()}
edgecolor = {edge: i_to_rgb(network.node_attribute(edge[0], 'cluster') / 9) for edge in network.edges()}

artist.draw_nodes(color=nodecolor)
artist.draw_edges(color=edgecolor)
