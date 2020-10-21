import os
from sklearn.cluster import KMeans
from numpy import array

from compas.geometry import Pointcloud
from compas.geometry import centroid_points
from compas.datastructures import Network


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'clusters.json')

network = Network()
network.update_default_node_attributes({'cluster': None, 'base': False})

cloud = Pointcloud.from_bounds(10, 5, 3, 100)
kmeans = KMeans(n_clusters=10, n_init=2000, max_iter=1000).fit(array(cloud, dtype=float))

clusters = {}
for i, point in zip(kmeans.labels_, cloud):
    print(i)
    if i not in clusters:
        clusters[i] = []
    clusters[i].append(point)

for index in clusters:
    nodes = []
    for point in clusters[index]:
        node = network.add_node(x=point[0], y=point[1], z=point[2], cluster=index)
        nodes.append(node)
    x, y, z = centroid_points(clusters[index])
    base = network.add_node(x=x, y=y, z=z, cluster=index, base=True)
    for node in nodes:
        network.add_edge(base, node)

network.to_json(FILE)
