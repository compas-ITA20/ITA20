# flake8: noqa

X0 = deepcopy(X)

for i in range(n):

    for j in i_nbrs[i]:

        f = ij_force[i, j]
        l = length_vector(subtract_vectors(b, a))

        X[i][0] = X0[i][0] + 0.1 * f * (X0[j][0] - X0[i][0]) / l
        X[i][1] = X0[i][1] + 0.1 * f * (X0[j][1] - X0[i][1]) / l
        X[i][2] = X0[i][2] + 0.1 * f * (X0[j][2] - X0[i][2]) / l
