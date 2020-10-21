import compas
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

network = Network.from_obj(compas.get('grid_irregular.obj'))

plotter = NetworkPlotter(network, figsize=(10, 8))

plotter.draw_nodes(radius=0.1, picker=10)
plotter.draw_edges()

default_colors = [plotter.defaults['node.facecolor'] for key in network.nodes()]
highlight_color = '#ff0000'

default_linewidths = [plotter.defaults['edge.width'] for key in network.edges()]
highlight_width = 3 * plotter.defaults['edge.width']

index_node = network.index_key()
edge_index = network.uv_index()
edge_index.update({(v, u): index for (u, v), index in edge_index.items()})


def on_pick(event):
    index = event.ind[0]
    node = index_node[index]

    colors = default_colors[:]
    colors[node] = highlight_color

    widths = default_linewidths[:]

    for nbr in network.neighbors(node):
        colors[nbr] = highlight_color
        widths[edge_index[node, nbr]] = highlight_width

    plotter.nodecollection.set_facecolor(colors)
    plotter.edgecollection.set_linewidths(widths)
    plotter.update()


plotter.register_listener(on_pick)
plotter.show()
