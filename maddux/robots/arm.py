"""
A robot arm
"""

import numpy as np

class Arm:

    def __init__(self, links, q0, name):
        """
        :param links: Vector of Link objects (1xN numpy vector)
        :param q0: The default (resting state) joint configuration (1xN numpy vector)
        :param name: Name of the arm
        """
        self.n = links.size
        self.links = links
        self.q0 = q0
        self.name = name

        self.base = np.identity(4)
        self.tool = np.identity(4)

    """
    Updates the given link's angle with the given angle
    :param link: The link you want to update, given as a integer
    :param new_angle: The link's new angle
    """
    def update_link_angle(self, link, new_angle):
        self.links[link].theta = new_angle

    """
    Resets the arm back to its resting state, i.e. q0
    """
    def reset(self):
      for link, q in zip(self.links, self.q0):
        link.set_theta(q)

    """
    Computes the forward kinematics of the arm using the current joint
    configuration or a given joint configuration
    :param q: Optional joint configuration to compute the FK on (1xN numpy vector)
    """
    def fkine(self, q=None):
        t = self.base
        for i, link in enumerate(self.links):
            if q:
                t = t * link.compute_transformation_matrix(q[i])
            else:
                t = t * link.transform_matrix
        t = t * self.tool
        return t
