from math import radians

from compas.geometry import Pointcloud
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import Frame
from compas.geometry import Point, Vector, Line
from compas.geometry import closest_point_on_line
from compas.rpc import Proxy

import compas_rhino
from compas_rhino.artists import PointArtist
from compas_rhino.artists import FrameArtist
from compas_rhino.artists import LineArtist


numerical = Proxy('compas.numerical')

pcl = Pointcloud.from_bounds(10, 5, 3, 100)

Rz = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(60))
Ry = Rotation.from_axis_and_angle([0.0, 1.0, 0.0], radians(20))
Rx = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], radians(10))

T = Translation.from_vector([2.0, 5.0, 8.0])

pcl.transform(T * Rz * Ry * Rx)

PointArtist.draw_collection(pcl, layer="ITA20::PCL", clear=True)
