import bpy
import time


ob = bpy.context.object

ob.location[0] = 0
bpy.context.view_layer.update()
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

for i in range(10):
    time.sleep(0.5)
    ob.location[0] += 1.0
    bpy.context.view_layer.update()
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)