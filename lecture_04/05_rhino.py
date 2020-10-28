from __future__ import print_function

import rhinoscriptsyntax as rs
import scriptcontext as sc
import compas_rhino

guids = compas_rhino.get_objects()
compas_rhino.delete_objects(guids, True)

result = rs.AddBox([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])

print(result)

obj = sc.doc.Objects.Find(result)

print(obj)
