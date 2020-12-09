import os
import json

from compas.geometry import Box
from compas.geometry import dot_vectors
from compas.geometry import Frame, Transformation
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

world = Frame.worldXY()

for guid in guids:
    surface = RhinoSurface.from_guid(guid)
    block = surface.to_compas()
    block.name = str(guid)

    bottom = sorted(block.faces(), key=lambda face: dot_vectors(block.face_normal(face), [0, 0, -1]))[-1]

    plane = block.face_centroid(bottom), [0, 0, 1]
    frame = Frame.from_plane(plane)

    T = Transformation.from_frame_to_frame(frame, world)

    block.transform(T)

    blank = Box.from_bounding_box(block.bounding_box())
    blank.xsize += 25
    blank.ysize += 25
    blank.zsize += 25

    block.attributes['blank'] = blank
    block.attributes['bottom'] = bottom

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
    artist.draw_faces(color={block.attributes['bottom']: (255, 0, 0)})

    blank = block.attributes['blank']

    artist = BoxArtist(blank, layer="ITA20::Assignment1::{}::Blank".format(block.name))
    artist.draw(show_edges=True, show_faces=False)
