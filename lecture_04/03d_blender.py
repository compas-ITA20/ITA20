import bpy

for block in bpy.data.meshes:
    print(f"mesh: {block.name}\n")

for block in bpy.data.objects:
    print(f"object: {block.name}")
    print(f"type: {block.type}")
    print(f"data: {block.data}\n")

for block in bpy.data.collections:
    print(f"collection: {block.name}")
    print(f"objects: {block.objects}")
