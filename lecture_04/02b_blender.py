from random import choice
import compas
from compas.datastructures import Network
from compas.topology import shortest_path
from compas.utilities import pairwise
from compas_plotters import NetworkPlotter


def on_pick(event):
    index = event.ind[0]
    start = index_node[index]
    nodes = shortest_path(network.adjacency, start, goal)
    colors = default_colors[:]
    widths = default_linewidths[:]
    colors[start] = highlight_color
    for u, v in pairwise(nodes):
        colors[v] = highlight_color
        widths[edge_index[u, v]] = highlight_width
    plotter.nodecollection.set_facecolor(colors)
    plotter.edgecollection.set_linewidths(widths)
    plotter.update()


network = Network.from_obj(compas.get('grid_irregular.obj'))
goal = choice(list(network.leaves()))

index_node = network.index_key()
edge_index = network.uv_index()
edge_index.update({(v, u): index for (u, v), index in edge_index.items()})

plotter = NetworkPlotter(network, figsize=(10, 8))
plotter.draw_nodes(radius=0.1, picker=10)
plotter.draw_edges()

default_colors = [(1, 1, 1) for key in network.nodes()]
highlight_color = (1, 0, 0)
default_colors[goal] = highlight_color
default_linewidths = [1.0 for key in network.edges()]
highlight_width = 3.0

plotter.nodecollection.set_facecolor(default_colors)
plotter.register_listener(on_pick)
plotter.show()
