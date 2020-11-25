import math

from compas.robots import RobotModel
from compas.robots import Joint

from compas.datastructures import Mesh
from compas.geometry import Frame, Point, Vector, Circle, Plane, Line
from compas.geometry import Cylinder, Box
from compas.geometry import Translation, Transformation

from compas.utilities import pairwise
from compas.utilities import linspace
from compas.utilities import remap_values

import compas_rhino
from compas_rhino.artists import FrameArtist, LineArtist, CylinderArtist
from compas_rhino.artists import RobotModelArtist

robot = RobotModel('tom')

# ==============================================================================
# Links
# ==============================================================================

cylinder = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 0.5), 0.02)
mesh = Mesh.from_shape(cylinder, u=32)
base = robot.add_link(
    'base',
    visual_meshes=[mesh],
    visual_color=(0.1, 0.1, 0.1)
)

cylinder = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 0.2), 0.5)
cylinder.transform(Translation.from_vector([0, 0, 0.25]))
mesh = Mesh.from_shape(cylinder, u=24)
shoulder = robot.add_link(
    'shoulder',
    visual_meshes=[mesh],
    visual_color=(0, 0, 1.0)
)

cylinder = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 0.08), 1.0)
cylinder.transform(Translation.from_vector([0, 0, 0.5]))
mesh = Mesh.from_shape(cylinder)
arm = robot.add_link(
    'arm',
    visual_meshes=[mesh],
    visual_color=(0.0, 1.0, 1.0)
)

cylinder = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 0.08), 1.0)
cylinder.transform(Translation.from_vector([0, 0, 0.5]))
mesh = Mesh.from_shape(cylinder)
forearm = robot.add_link(
    'forearm',
    visual_meshes=[mesh],
    visual_color=(0.0, 1.0, 1.0)
)

cylinder = Cylinder(Circle(Plane(Point(0, 0, 0), Vector(0, 0, 1)), 0.11), 0.01)
mesh = Mesh.from_shape(cylinder, u=32)
wrist = robot.add_link(
    'wrist',
    visual_meshes=[mesh],
    visual_color=(0.1, 0.1, 0.1)
)

box = Box.from_width_height_depth(0.04, 0.3, 0.22)
box.transform(Translation.from_vector([0, 0, 0.15]))
mesh = Mesh.from_shape(box)
hand = robot.add_link(
    'hand',
    visual_meshes=[mesh],
    visual_color=(0, 0, 1.0)
)

# ==============================================================================
# Joints
# ==============================================================================

base_joint = robot.add_joint(
    'base-shoulder',
    Joint.REVOLUTE,
    base, shoulder,
    origin=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 0, 1),
    limit=(-0.5 * math.pi, +0.5 * math.pi)
)

shoulder_joint = robot.add_joint(
    'shoulder-arm',
    Joint.REVOLUTE,
    shoulder, arm,
    origin=Frame(Point(0, 0, 0.5), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 1, 0),
    limit=(-0.5 * math.pi, +0.5 * math.pi)
)

elbow_joint = robot.add_joint(
    'arm-forearm',
    Joint.REVOLUTE,
    arm, forearm,
    origin=Frame(Point(0, 0, 1.0), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 1, 0),
    limit=(-0.5 * math.pi, +0.5 * math.pi)
)

wrist_joint = robot.add_joint(
    'forearm-wrist',
    Joint.REVOLUTE,
    forearm, wrist,
    origin=Frame(Point(0, 0, 1.0), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 1, 0),
    limit=(-0.5 * math.pi, +0.5 * math.pi)
)

hand_joint = robot.add_joint(
    'wrist-hand',
    Joint.CONTINUOUS,
    wrist, hand,
    origin=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 0, 1)
)

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

    artist = RobotModelArtist(robot, layer="Robot")
    artist.clear_layer()
    artist.update(state, collision=False)
    artist.draw()

    compas_rhino.wait()
