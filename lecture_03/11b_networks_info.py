import compas
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

network = Network.from_obj(compas.get('grid_irregular.obj'))

plotter = NetworkPlotter(network, figsize=(12, 7.5))
plotter.draw_nodes(facecolor={node: (255, 0, 0) for node in network.leaves()})
plotter.draw_edges()
plotter.show()
