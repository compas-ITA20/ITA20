# stoire block as data

import os

from compas.datastructures import Mesh
from compas.geometry import Box

import compas_rhino
from compas_rhino.artists import BoxArtist, MeshArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'data', 'block.json')

# ==============================================================================
# Make a block from a box
# ==============================================================================

box = Box.from_width_height_depth(600, 200, 300)
block = Mesh.from_shape(box)

# ==============================================================================
# Define blank as block bounding box with padding
# ==============================================================================

blank = Box.from_bounding_box(block.bounding_box())
blank.xsize += 50
blank.ysize += 50
blank.zsize += 50

# ==============================================================================
# Store blank as attribute of block
# ==============================================================================

block.attributes['blank'] = blank

# ==============================================================================
# Export
# ==============================================================================

block.to_json(FILE)

# ==============================================================================
# Visualize
# ==============================================================================

compas_rhino.clear()

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces()

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)
