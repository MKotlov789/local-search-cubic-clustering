import math
from numpy.linalg import norm
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from numpy import dot


class _BaseGreedyClustering:
    """
        Base class for greedy clustering algorithms.

        Parameters:
        instance (object): An instance of the clustering problem containing the following attributes:
            - node_num (int): The number of nodes.
            - costs (numpy.ndarray): The cost matrix.
            - nodes (numpy.ndarray): The node coordinates.
            - triplets (list): List of triplets indicating node indices for triplet constraints.
            - mean_sq (callable): Mean square optimization function.
            - normals (numpy.ndarray): Normal vectors for nodes.
            - nodes_partition (list): List of node partitions after clustering.
            - angle_dif (list): List of angle differences between original normals and optimized normals.
        Methods:
            - plot(): Plots the clustered nodes in 3D space.
            - compute_angle_dif(): Computes angle differences between original normals and optimized normals.
        """
    def __init__(self, instance):
        """
        Initialize the BaseGreedyClustering instance.

        Args:
        instance (object): An instance of the clustering problem.
        """
        self.angle_dif = None
        self.node_number = instance.node_number
        self.costs = instance.costs
        self._nodes_index_partition = []
        self.nodes_partition = None
        self.nodes = instance.nodes
        self._triplets = instance.triplets
        self._opt_function = instance.mean_sq
        self.normals = instance.normals



    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        for nodes_set in self.nodes_partition:
            ax.scatter(nodes_set[0], nodes_set[1], nodes_set[2])
        plt.show()

    def _index_to_node(self, index_partition):
        nodes_transposed = np.transpose(self.nodes)
        nodes_partition = []
        for index_collection in range(len(index_partition)):
            nodes_collection = np.array([])
            for index in index_partition[index_collection]:
                nodes_collection = np.append(nodes_collection, nodes_transposed[index])
            nodes_collection = nodes_collection.reshape((-1, 3))
            nodes_collection = np.transpose(nodes_collection)
            nodes_partition.append(nodes_collection)
        return nodes_partition

    def _find_normals(self):
        nodes_partition = self._index_to_node(self._nodes_index_partition)
        self._new_normals = []
        for node in nodes_partition:
            if len(node[0]) >= 3:
                A = np.transpose(node)
                res = optimize.least_squares(self._opt_function,
                                             np.array([1, 1, 1]), 
                                             args=((A,)),
                                             bounds=(-1., 1.))
                self._new_normals.append(res.x)

    def compute_angle_dif(self):
        self._find_normals()
        angle_dif = []
        for normal in self.normals:
            results = []
            if len(self._new_normals) == 0:
                break
            for vector in self._new_normals:
                angle = dot(normal, vector) / (norm(normal) * norm(vector))
                if abs(angle) >= 1:
                    angle = 1
                dif = math.degrees(math.acos(angle))
                results.append(min(abs(dif), abs(180 - dif)))
            angle_dif.append(min(results))
        self.angle_dif = angle_dif