import os
import math

from compas.robots import RobotModel

from compas.geometry import Frame, Point, Vector, Circle, Plane, Line
from compas.geometry import Cylinder
from compas.geometry import Transformation

from compas.utilities import pairwise
from compas.utilities import linspace
from compas.utilities import remap_values

import compas_rhino
from compas_rhino.artists import FrameArtist, LineArtist, CylinderArtist

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'data', 'robot.json')

robot = RobotModel.from_json(FILE)

# ==============================================================================
# States
# ==============================================================================

names = robot.get_configurable_joint_names()
joints = list(robot.iter_joints())
motions = []

space = list(linspace(0, 1, 100))

for joint in joints:
    if joint.limit:
        lower = joint.limit.lower
        upper = joint.limit.upper
    else:
        lower = 0
        upper = 2 * math.pi
    motion = remap_values(space, target_min=lower, target_max=upper)
    motions.append(motion)

for values in zip(*motions):
    state = dict(zip(names, values))
    transformations = robot.compute_transformations(state)

    frames = []
    axes = []

    for joint in joints:
        frame = joint.origin.transformed(transformations[joint.name])
        frame.name = joint.name
        frames.append(frame)

        axis = joint.axis.transformed(transformations[joint.name])
        axis.name = joint.name
        axes.append(axis)

    # Visualization

    for frame in frames:
        artist = FrameArtist(frame, scale=0.3, layer="Frames::{}".format(frame.name))
        artist.clear_layer()
        artist.draw()

    for a, b in pairwise(frames):
        line = Line(a.point, b.point)
        artist = LineArtist(line, layer="Links::{}".format(a.name))
        artist.draw()

    tpl = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 0.05), 0.2)
    for frame, axis in zip(frames, axes):
        point = frame.point
        normal = Vector(axis.x, axis.y, axis.z)
        plane = Plane(point, normal)
        frame = Frame.from_plane(plane)
        X = Transformation.from_frame(frame)
        cylinder = tpl.transformed(X)
        artist = CylinderArtist(cylinder, layer="Axes::{}".format(axis.name))
        artist.clear_layer()
        artist.draw()

    compas_rhino.rs.Redraw()
    compas_rhino.wait()
