import os
import json

from compas.geometry import Box
from compas.utilities import DataEncoder

import compas_rhino
from compas_rhino.artists import BoxArtist, MeshArtist
from compas_rhino.geometry import RhinoSurface

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'data', 'blocks.json')

# ==============================================================================
# Blocks and Blanks
# ==============================================================================

guids = compas_rhino.select_surfaces()

blocks = []

for guid in guids:
    surface = RhinoSurface.from_guid(guid)
    block = surface.to_compas()
    block.name = str(guid)

    blank = Box.from_bounding_box(block.bounding_box())
    blank.xsize += 25
    blank.ysize += 25
    blank.zsize += 25

    block.attributes['blank'] = blank

    blocks.append(block)

# ==============================================================================
# Export
# ==============================================================================

with open(FILE, 'w') as f:
    json.dump(blocks, f, cls=DataEncoder)

# ==============================================================================
# Visualize
# ==============================================================================

compas_rhino.clear_layers(["ITA20::Assignment1"])

for block in blocks:
    artist = MeshArtist(block, layer="ITA20::Assignment1::{}::Block".format(block.name))
    artist.draw_faces()

    blank = block.attributes['blank']

    artist = BoxArtist(blank, layer="ITA20::Assignment1::{}::Blank".format(block.name))
    artist.draw(show_edges=True, show_faces=False)
