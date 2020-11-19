import os

from compas.geometry import Box
from compas.datastructures import Mesh

import compas_rhino
from compas_rhino.artists import BoxArtist, MeshArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_O = os.path.join(HERE, 'data', 'block.json')

# ==============================================================================
# Block and Blank
# ==============================================================================

box = Box.from_width_height_depth(200, 200, 200)
block = Mesh.from_shape(box)

vertex = next(block.vertices_where({'x': (float('-inf'), 0), 'y': (0, float('inf')), 'z': (0, float('inf'))}))
block.vertex_attribute(vertex, 'z', 120)

vertex = next(block.vertices_where({'x': (0, float('inf')), 'y': (0, float('inf')), 'z': (0, float('inf'))}))
block.vertex_attribute(vertex, 'z', 150)

blank = Box.from_bounding_box(block.bounding_box())
blank.xsize += 20
blank.ysize += 20
blank.zsize += 20

block.attributes['blank'] = blank

# ==============================================================================
# Export
# ==============================================================================

block.to_json(FILE_O)

# ==============================================================================
# Visualize
# ==============================================================================

compas_rhino.clear()

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces()

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)
