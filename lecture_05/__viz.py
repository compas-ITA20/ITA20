import compas_rhino
from compas.geometry import length_vector, add_vectors
from compas.geometry import scale_vector
from compas.geometry import Cylinder
from compas_rhino.artists import CylinderArtist
from compas_rhino.artists import MeshArtist


class CablenetArtist(MeshArtist):

    def draw_reactions(self, color=(0, 255, 0), scale=0.1):
        lines = []
        for vertex in self.mesh.vertices():
            if not self.mesh.vertex_attribute(vertex, 'is_anchor'):
                continue
            start = self.mesh.vertex_attributes(vertex, 'xyz')
            residual = self.mesh.vertex_attributes(vertex, ['rx', 'ry', 'rz'])
            end = add_vectors(start, scale_vector(residual, -scale))
            lines.append({
                'start': start,
                'end': end,
                'arrow': 'end',
                'color': color
            })
        compas_rhino.draw_lines(lines, layer=self.layer)

    def draw_residuals(self, color=(0, 255, 255), tol=0.001):
        lines = []
        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, 'is_anchor'):
                continue
            start = self.mesh.vertex_attributes(vertex, 'xyz')
            residual = self.mesh.vertex_attributes(vertex, ['rx', 'ry', 'rz'])
            end = add_vectors(start, residual)
            if length_vector(residual) < tol:
                continue
            lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})
        compas_rhino.draw_lines(lines, layer=self.layer)

    def draw_forces(self, color=(255, 0, 0), scale=0.1, tol=0.001):
        for edge in self.mesh.edges():
            q = self.mesh.edge_attribute(edge, 'q')
            l = self.mesh.edge_length(*edge)  # noqa E741
            f = q * l
            radius = scale * f
            if radius < tol:
                continue
            mp = self.mesh.edge_midpoint(*edge)
            direction = self.mesh.edge_direction(*edge)
            height = l
            cylinder = Cylinder(((mp, direction), radius), height)
            artist = CylinderArtist(cylinder, layer=self.layer, color=color)
            artist.draw(u=16)

    def draw_loads(self, color=(0, 255, 0), scale=0.1):
        lines = []
        for vertex in self.mesh.vertices_where({'is_anchor': False}):
            start = self.mesh.vertex_attributes(vertex, 'xyz')
            load = self.mesh.vertex_attributes(vertex, ['px', 'py', 'pz'])
            end = add_vectors(start, scale_vector(load, scale))
            lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})
        compas_rhino.draw_lines(lines, layer=self.layer)
