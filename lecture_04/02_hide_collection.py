import bpy

for collection in bpy.context.scene.collection.children:
    print(collection.name)

bpy.context.scene.collection.children['Collection'].hide_viewport = False