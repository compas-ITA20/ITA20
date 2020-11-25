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

base_joint = robot.add_joint('base-shoulder', Joint.REVOLUTE, base, shoulder)
shoulder_joint = robot.add_joint('shoulder-arm', Joint.REVOLUTE, shoulder, arm)
elbow_joint = robot.add_joint('arm-forearm', Joint.REVOLUTE, arm, forearm)
wrist_joint = robot.add_joint('forearm-wrist', Joint.REVOLUTE, forearm, wrist)
hand_joint = robot.add_joint('wrist-hand', Joint.CONTINUOUS, wrist, hand)

# ==============================================================================
# Visualization
# ==============================================================================

print(robot)
