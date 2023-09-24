import numpy as np
from scipy.spatial.transform import Rotation


class Plane:
    """
    A class representing a plane in 3D space.

    Attributes:
        node_number (int): The number of nodes on the plane.
        alpha_angle (float): The alpha angle of rotation (degrees).
        beta_angle (float): The beta angle of rotation (degrees).
        normal_vector (tuple): The normal vector of the plane.
        deviation (float): The deviation used for adding noise to node coordinates.
        nodes (numpy.ndarray): An array containing the 3D coordinates of nodes on the plane.

    Methods:
        __init__(self, node_number, angles, deviation):
            Initializes a Plane object with the given parameters.

        _rotate(self):
            Rotates the plane's node coordinates and normal vector based on alpha and beta angles.

        _add_noise(self):
            Adds noise to the node coordinates.

    Usage Example:
        plane = Plane(node_number=100, angles=[30, 45], deviation=0.1)
    """

    def __init__(self, node_number, angles, deviation):
        """
        Initializes a Plane object with the given parameters.

        Args:
            node_number (int): The number of nodes on the plane.
            angles (list): A list containing the alpha and beta angles of rotation (degrees).
            deviation (float): The deviation used for adding noise to node coordinates.
        """
        self.node_number = node_number
        self.alpha_angle = angles[0]
        self.beta_angle = angles[1]

        self.normal_vector = (0, 0, 1)
        self.deviation = deviation
        x_coordinates_2d = np.random.uniform(-1, 1, self.node_number)
        y_coordinates_2d = np.random.uniform(-1, 1, self.node_number)
        node_coordinates_2d = np.append([x_coordinates_2d], [y_coordinates_2d], axis=0)

        self.nodes = np.append(node_coordinates_2d, np.full((1, self.node_number), 0), axis=0)
        self._add_noise()
        self._rotate()

    def _rotate(self):
        """
        Rotates the plane's node coordinates and normal vector based on alpha and beta angles.
        """
        rotation = Rotation.from_euler('zyx', [0, self.alpha_angle, self.beta_angle], degrees=True)
        rotation_matrix = rotation.as_matrix()
        self.nodes = np.matmul(rotation_matrix, self.nodes)
        self.normal_vector = np.matmul(rotation_matrix, self.normal_vector)
        self.nodes = np.transpose(np.transpose(self.nodes) - np.mean(self.nodes, 1))

    def _add_noise(self):
        """
        Adds noise to the node coordinates.
        """
        noise = self.nodes.shape[1]
        noise = np.append(np.zeros((2, noise)), np.random.normal(0, self.deviation, (1, noise)) / 10, axis=0)
        self.nodes += noise