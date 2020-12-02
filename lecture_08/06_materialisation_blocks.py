import os
import compas
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)

FILE_I1 = os.path.join(HERE, 'data', 'form_idos.json')
FILE_I2 = os.path.join(HERE, 'data', 'form_edos.json')

FILE_O = os.path.join(HERE, 'data', 'form_blocks.json')

idos = Mesh.from_json(FILE_I1)
edos = Mesh.from_json(FILE_I2)

blocks = []

for face in idos.faces():
    bottom = idos.face_coordinates(face)
    top = edos.face_coordinates(face)

    f = len(bottom)

    faces = [
        list(range(f)),
        list(range(f + f - 1, f - 1, -1))]

    for i in range(f - 1):
        faces.append([i, i + f, i + f + 1, i + 1])
    faces.append([f - 1, f + f - 1, f, 0])

    block = Mesh.from_vertices_and_faces(bottom + top, faces)
    blocks.append(block)


compas.json_dump(blocks, FILE_O)

artist = MeshArtist(None, layer="RV2::Blocks")
artist.clear_layer()

for block in blocks:
    artist.mesh = block
    artist.draw_faces(color=(0, 255, 255), join_faces=True)
