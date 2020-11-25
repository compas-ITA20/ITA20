import math

from compas.geometry import Point, Vector, Frame, Circle, Plane, Line
from compas.geometry import Cylinder
from compas.geometry import Transformation

from compas.utilities import pairwise

from compas.robots import RobotModel
from compas.robots import Joint

from compas_rhino.artists import FrameArtist, LineArtist, CylinderArtist

# ==============================================================================
# Model
# ==============================================================================

robot = RobotModel('tom')

# ==============================================================================
# Links
# ==============================================================================

base = robot.add_link('base')
shoulder = robot.add_link('shoulder')
arm = robot.add_link('arm')
forearm = robot.add_link('forearm')
wrist = robot.add_link('wrist')
hand = robot.add_link('hand')

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
    origin=Frame(Point(0, 0, 1.5), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 1, 0),
    limit=(-0.5 * math.pi, +0.5 * math.pi)
)

wrist_joint = robot.add_joint(
    'forearm-wrist',
    Joint.REVOLUTE,
    forearm, wrist,
    origin=Frame(Point(0, 0, 2.5), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 1, 0),
    limit=(-0.5 * math.pi, +0.5 * math.pi)
)

hand_joint = robot.add_joint(
    'wrist-hand',
    Joint.CONTINUOUS,
    wrist, hand,
    origin=Frame(Point(0, 0, 2.5), Vector(1, 0, 0), Vector(0, 1, 0)),
    axis=Vector(0, 0, 1)
)

# ==============================================================================
# State
# ==============================================================================

frames = []
axes = []

for joint in robot.iter_joints():
    frame = joint.origin
    frame.name = joint.name
    frames.append(frame)

    axis = joint.axis
    axis.name = joint.name
    axes.append(axis)

# ==============================================================================
# Visualization
# ==============================================================================

for frame in frames:
    artist = FrameArtist(frame, scale=0.3, layer="Frames::{}".format(frame.name))
    artist.clear_layer()
    artist.draw()

for a, b in pairwise(frames):
    line = Line(a.point, b.point)
    artist = LineArtist(line, layer="Links::{}".format(a.name))
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
