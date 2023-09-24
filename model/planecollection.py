import numpy as np
from matplotlib import pyplot as plt


class PlaneCollection:
    def __init__(self, *planes):
        self.nodes = [[], [], []]
        self.node_number = 0
        self.angles = []
        self.normals = []

        for plane in planes:
            self.nodes = np.append(self.nodes, plane.nodes, 1)
            self.node_number = self.node_number + plane.node_number
            self.angles.append([plane.alpha_angle, plane.beta_angle])
            self.normals.append(plane.normal_vector)
        self.nodes = np.transpose(self.nodes)
        np.random.shuffle(self.nodes)
        self.nodes = np.transpose(self.nodes)

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.scatter(self.nodes[0], self.nodes[1], self.nodes[2])
        for normal in self.normals:
            ax.quiver(0, 0, 0, normal[0], normal[1], normal[2])

        plt.show()