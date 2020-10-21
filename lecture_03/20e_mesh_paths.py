import random
import compas
from compas.datastructures import Mesh
from compas.topology import shortest_path
from compas.utilities import pairwise
from compas_plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

start, goal = random.choices(mesh.vertices_on_boundary(), k=2)

vertices = shortest_path(mesh.adjacency, start, goal)

vertexcolor = {start: (255, 0, 0)}
edgecolor = {}

for u, v in pairwise(vertices):
    vertexcolor[v] = (0, 255, 0)
    edgecolor[u, v] = (0, 255, 0)
    edgecolor[v, u] = (0, 255, 0)

vertexcolor[goal] = (0, 0, 255)

plotter = MeshPlotter(mesh, figsize=(12, 7.5))
plotter.draw_vertices(facecolor=vertexcolor)
plotter.draw_faces()
plotter.draw_edges(keys=list(pairwise(vertices)), color=edgecolor, width=2.0)
plotter.show()
