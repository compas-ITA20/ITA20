import bpy

for name in dir(bpy.data):
    if not name.startswith('_'):
        print(name)
