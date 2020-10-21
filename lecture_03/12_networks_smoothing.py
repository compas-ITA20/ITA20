import compas
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

network = Network.from_obj(compas.get('lines_noleaves.obj'))
plotter = NetworkPlotter(network, figsize=(12, 7.5))

corners = list(network.nodes_where({'degree': 2}))

# network.smooth(fixed=corners)

plotter.draw_nodes(facecolor={node: (255, 0, 0) for node in corners})
plotter.draw_edges()
plotter.show()
