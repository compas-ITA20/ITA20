import os
import bpy

FILE = bpy.context.space_data.text.filepath
HERE = os.path.dirname(FILE)

print(HERE)
