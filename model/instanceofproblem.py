import itertools
import math

from scipy import optimize
import numpy as np


class InstanceOfProblem:
    """
     A class representing an instance of a problem.

     This class provides methods to define distances, costs, and perform calculations on the instance data.

     Attributes:
     - node_num (int): Number of nodes in the instance.
     - nodes (numpy.ndarray): Array of node coordinates.
     - constant (float): A constant value used in cost calculations.
     - triplets (list): List of node triplets.
     - distances (list): List of distances between node triplets.
     - normals (list): List of normals for plane collections.

     Methods:
     - mean_sq(X, W): Calculates mean square values.
     - _define_distances(): Defines distances between node triplets.
     - _define_costs(): Defines costs for triplets based on distances.
     """

    def __init__(self, plane_collection=None, constant=None, nodes=None, distances=None, normals=None):
        """
                Initializes an instance of the problem.

                Args:
                - plane_collection (PlaneCollection): An optional PlaneCollection instance.
                - constant (float): A constant value used in cost calculations.
                - nodes (numpy.ndarray): Array of node coordinates.
                - distances (list): List of distances between node triplets.
                - normals (list): List of normals for plane collections.
                """
        if plane_collection is not None and constant is not None:
            self.node_number = plane_collection.node_number
            self.nodes = plane_collection.nodes
            self.constant = constant
            self.triplets = list(itertools.combinations(range(self.node_number), 3))
            self._define_distances()
            self._define_costs()
            self.normals = plane_collection.normals
        elif nodes is not None and distances is not None and normals is not None and constant is not None:
            self.nodes = nodes
            self.node_number = nodes.shape[1]
            self.constant = constant
            self.triplets = list(itertools.combinations(range(self.node_number), 3))
            self.distances = distances
            self._define_costs()
            self.normals = normals
        else:
            self.node_number = None
            self.nodes = None
            self.constant = None
            self.triplets = None
            self.distances = None
            self.normals = None


    def mean_sq(self, X, W):
        res_array = []
        for i in range(W[0].size):
            res_array = np.append(res_array, np.dot(X, W[i]) / math.sqrt(np.dot(X, X)))
        return np.array(res_array)

    def _define_distances(self):
        nodes_transposed = np.transpose(self.nodes)
        self.triplets = list(itertools.combinations(range(self.node_number), 3))
        self.distances = []

        for triplet in self.triplets:
            node_triplet = np.array([])
            for node_num in triplet:
                node_triplet = np.append(node_triplet, nodes_transposed[node_num])
            node_triplet = node_triplet.reshape((3, 3))

            res = optimize.least_squares(self.mean_sq, np.array([1, 1, 1]), args=((node_triplet,)), bounds=(-1., 1.))
            sum_dist = []
            for node in node_triplet:
                sum_dist.append(abs(np.dot(res.x, node) / math.sqrt(np.dot(res.x, res.x))))

            self.distances.append(sum_dist)

    def _define_costs(self):
        self.costs = {}
        const = self.constant
        for d in range(len(self.distances)):
            d1 = self.distances[d][0]
            d2 = self.distances[d][1]
            d3 = self.distances[d][2]

            c2 = max(d1 - const, d2 - const, d3 - const)
            # c1 = - min(0, c2)
            self.costs.update({self.triplets[d]: [0, c2]})
