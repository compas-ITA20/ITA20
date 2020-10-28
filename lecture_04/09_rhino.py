import compas_rhino
from compas.geometry import Point, Box, Sphere
from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas_rhino.artists import MeshArtist

proxy = Proxy()
# proxy.restart_server()

compas_rhino.clear()

box = Box.from_width_height_depth(2, 2, 2)
box = Mesh.from_shape(box)
box.quads_to_triangles()

A = box.to_vertices_and_faces()

sphere = Sphere(Point(1, 1, 1), 1)
sphere = Mesh.from_shape(sphere, u=30, v=30)
sphere.quads_to_triangles()

B = sphere.to_vertices_and_faces()

proxy.package = "compas_cgal.meshing"
B = proxy.remesh(B, 0.3, 10)

proxy.package = "compas_cgal.booleans"
V, F = proxy.boolean_union(A, B)

mesh = Mesh.from_vertices_and_faces(V, F)

artist = MeshArtist(mesh)
artist.draw_faces()
