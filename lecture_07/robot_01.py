import math

from compas.geometry import Point, Vector, Frame

from compas.robots import RobotModel
from compas.robots import Joint

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
# Visualization
# ==============================================================================

print(robot)
