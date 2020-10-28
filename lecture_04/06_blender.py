import time
import bpy
import compas_blender

compas_blender.clear()

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

obj = bpy.context.object

for i in range(10):
    time.sleep(0.5)
    obj.location[0] += 0.5
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
