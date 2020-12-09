import os
import math

from compas.geometry import Point, Vector, Frame, Circle, Plane, Line
from compas.geometry import Cylinder
from compas.geometry import Transformation
from compas.utilities import pairwise, linspace
from compas.robots import RobotModel

import compas_rhino
from compas_rhino.artists import FrameArtist, LineArtist, CylinderArtist

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'data', 'robot.json')

robot = RobotModel.from_json(FILE)

# ==============================================================================
# From frame
# ==============================================================================

base_joint = robot.get_joint_by_name('base-shoulder')
frame_from = base_joint.origin

# ==============================================================================
# State
# ==============================================================================

names = robot.get_configurable_joint_names()
values = [+0.25 * math.pi, -0.25 * math.pi, +0.5 * math.pi, 0, +0.25 * math.pi]
state = dict(zip(names, values))

for i in linspace(0, 10, 100):
    frame_to = Frame([i * 0.3, i * 0.3, 0], [1, 0, 0], [0, 1, 0])
    T = Transformation.from_frame_to_frame(frame_from, frame_to)

    transformations = robot.compute_transformations(state, parent_transformation=T)

    frames = []
    axes = []

    for joint in robot.iter_joints():
        frame = joint.origin.transformed(transformations[joint.name])
        frame.name = joint.name
        frames.append(frame)

        axis = joint.axis.transformed(transformations[joint.name])
        axis.name = joint.name
        axes.append(axis)

    for frame in frames:
        artist = FrameArtist(frame, scale=0.3, layer="Frames::{}".format(frame.name))
        artist.clear_layer()
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

    for a, b in pairwise(frames):
        line = Line(a.point, b.point)
        artist = LineArtist(line, layer="Links::{}".format(a.name))
        artist.draw()

    compas_rhino.rs.Redraw()
    compas_rhino.wait()
