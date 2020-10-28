import time
import rhinoscriptsyntax as rs
import scriptcontext as sc
import compas_rhino

guids = compas_rhino.get_objects()
compas_rhino.delete_objects(guids, True)

result = rs.AddBox([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])

obj = sc.doc.Objects.Find(result)
xform = rs.XformTranslation([0.5, 0, 0])
rs.Redraw()

for i in range(10):
    time.sleep(0.5)
    rs.TransformObject(obj, xform)
    rs.Redraw()
