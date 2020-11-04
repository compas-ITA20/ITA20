import compas_rhino
from compas.geometry import add_vectors, subtract_vectors, length_vector
from compas.datastructures import Network
from compas_rhino.artists import NetworkArtist


# visualisation functions

def draw_reactions(network, layer, color):
    lines = []
    for node in network.nodes_where({'is_anchor': True}):
        start = network.node_attributes(node, 'xyz')
        residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
        end = subtract_vectors(start, residual)
        lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})
    compas_rhino.draw_lines(lines, layer=layer)


def draw_residuals(network, layer, color, tol):
    lines = []
    for node in network.nodes_where({'is_anchor': False}):
        start = network.node_attributes(node, 'xyz')
        residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
        if length_vector(residual) < tol:
            continue
        end = add_vectors(start, residual)
        lines.append({'start': start, 'end': end, 'arrow': 'end', 'color': color})
    compas_rhino.draw_lines(lines, layer=layer)


# equilibrium functions

def update_R():
    for i in range(n):
        R[i] = [0, 0, 0]
        a = X[i]
        for j in i_nbrs[i]:
            b = X[j]
            f = ij_force[i, j]
            l = length_vector(subtract_vectors(b, a))  # noqa: E741
            R[i][0] += f * (b[0] - a[0]) / l
            R[i][1] += f * (b[1] - a[1]) / l
            R[i][2] += f * (b[2] - a[2]) / l


def update_X():
    for i in free:
        X[i][0] += 0.5 * R[i][0]
        X[i][1] += 0.5 * R[i][1]
        X[i][2] += 0.5 * R[i][2]


# clear the Rhino model
# and define the drawing helpers/parameters

compas_rhino.clear()

# create a network

network = Network()

network.update_dna(is_anchor=False)
network.update_dna(rx=0, ry=0, rz=0)
network.update_dea(f=1)

a = network.add_node(x=0, y=0, z=0, is_anchor=True)
b = network.add_node(x=10, y=0, z=10, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e, f=2)
network.add_edge(b, e)
network.add_edge(c, e)
network.add_edge(d, e)

# numerical data

n = network.number_of_nodes()
e = network.number_of_edges()

node_index = {node: index for index, node in enumerate(network.nodes())}

fixed = list(network.nodes_where({'is_anchor': True}))
free = list(network.nodes_where({'is_anchor': False}))

fixed[:] = [node_index[node] for node in fixed]
free[:] = [node_index[node] for node in free]

X = network.nodes_attributes('xyz')
R = network.nodes_attributes(['rx', 'ry', 'rz'])

i_nbrs = {node_index[node]: [node_index[nbr] for nbr in network.neighbors(node)] for node in network.nodes()}

ij_force = {}
for u, v in network.edges():
    i = node_index[u]
    j = node_index[v]
    force = network.edge_attribute((u, v), 'f')
    ij_force[i, j] = force
    ij_force[j, i] = force

# initialize

tol = 0.01
kmax = 100

update_R()

# run iterations

layer = "ITA20::L5::FormFinding"
artist = NetworkArtist(network, layer=layer)

for k in range(kmax):
    if k % 10 == 0:
        if sum(length_vector(R[i]) for i in free) < tol:
            break

    if k % 2 == 0:
        for node in network.nodes():
            index = node_index[node]
            network.node_attributes(node, ['x', 'y', 'z'], X[index])
            network.node_attributes(node, ['rx', 'ry', 'rz'], R[index])

        artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
        artist.draw_edges()

        draw_reactions(network, layer, (0, 255, 0))
        draw_residuals(network, layer, (0, 255, 255), tol)

        compas_rhino.rs.Redraw()
        compas_rhino.wait()

    update_X()
    update_R()

# update network

for node in network.nodes():
    index = node_index[node]
    network.node_attributes(node, ['x', 'y', 'z'], X[index])
    network.node_attributes(node, ['rx', 'ry', 'rz'], R[index])

# visualize result

artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
artist.draw_edges()

draw_reactions(network, layer, (0, 255, 0))
draw_residuals(network, layer, (0, 255, 255), tol)
