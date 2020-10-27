import os
import sys
import bpy
import time

HERE = os.path.dirname(__file__)
print(HERE)
print(os.path.dirname(bpy.path.abspath("//")))
print(bpy.context.space_data.text.filepath)

print(sys.version_info)
print(sys.executable)

print(bpy.app.binary_path)
print(bpy.app.binary_path_python)
print(bpy.app.tempdir)

print(dir(bpy.data))

# the scene has a default/root collection
# it does not show up in the data
# it is built-in

# bpy.context.window.view_layer.layer_collection.children["Some Collection"].exclude = True

ob = bpy.context.object
ob.location[0] -= 100

for i in range(10):
    ob.location[0] += 1
    time.sleep(1)
    bpy.context.view_layer.update()

print(bpy.context.active_object.name)

# this is the last object involved in an operation
print(bpy.context.active_object is bpy.context.object)

ob = bpy.context.object
print(ob.name)

ob.hide_viewport = False

if not ob.select_get():
    ob.select_set(True)


ob = bpy.context.object
print("Object %s:\n\thide in viewport: %r\n\thide in render: %r\n\tis selectable: %r\n" %
      (ob.name, ob.hide_viewport, ob.hide_render, not ob.hide_select))