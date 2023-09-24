import numpy as np

from algorithm.greedymovingkl import GreedyMovingKl
from model.instanceofproblem import InstanceOfProblem
from model.plane import Plane
from model.planecollection import PlaneCollection


def test(iter, pr):
    time = []
    angles = []
    n_plane = []
    for i in range(iter):
        sol = GreedyMovingKl(pr)
        sol.do_clustering(measure_time=True)
        n_plane.append(len(sol.partition))
        time.append(sol.time)
        sol.angle_dif()
        # sol.plot()
        for angle in sol.angle_d:
            angles.append(angle)
    print(sum(time) / len(time))
    print(sum(n_plane) / len(n_plane))
    print(sum(angles) / len(angles))


#
pl1 = Plane(8, [0, 90], 0)
pl2 = Plane(8, [90, 0], 0)
# pl3 = Plane(20, [110,0], 0.1)
# pl4 = Plane(15, [60,45], 0.1)
# pl5 = Plane(15, [0,135], 0.1)
inst = PlaneCollection(pl1, pl2)
# inst.plot()
pr = InstanceOfProblem(inst, 0.02)
X_file = open("data/16.txt", "w")
d_file = open("data/d16.txt", "w")
n_file = open("data/n16.txt", "w")
np.savetxt(X_file,pr.nodes.reshape(-1))
np.savetxt(d_file,pr.distances)
np.savetxt(n_file, pr.normals)
X_file.close()
d_file.close()
n_file.close()
#
nodes = np.loadtxt("data/16.txt").reshape(3, -1)
distances = np.loadtxt("data/d16.txt")
normals = np.loadtxt("data/n16.txt")

inst_of_pr = InstanceOfProblem(None, 0.03, nodes, distances, normals)

sol = GreedyMovingKl(inst_of_pr)
sol.do_clustering(measure_time=True)
print(len(sol.nodes_partition))
print(sol.time)
sol.compute_angle_dif()
print(sol.angle_dif)
sol.plot()
# # test(5,pr)
