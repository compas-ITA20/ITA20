import bpy
import compas_blender

compas_blender.clear()

result = bpy.ops.mesh.primitive_cube_add(size=1)

print(result)
