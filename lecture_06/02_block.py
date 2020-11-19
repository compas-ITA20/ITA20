# sanity check of data

import os

from compas.datastructures import Mesh

import compas_rhino
from compas_rhino.artists import BoxArtist, MeshArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'data', 'block.json')

# ==============================================================================
# Load data
# ==============================================================================

block = Mesh.from_json(FILE)
blank = block.attributes['blank']

# ==============================================================================
# Visualize
# ==============================================================================

compas_rhino.clear()

artist = MeshArtist(block, layer="ITA20::HotWire::Block")
artist.draw_faces()

artist = BoxArtist(blank, layer="ITA20::HotWire::Blank")
artist.draw(show_edges=True, show_faces=False)
