"""
A robot arm
"""

import numpy as np
import utils

class Arm:

    def __init__(self, links, q0, name):
        """
        :param links: Vector of Link objects (1xN numpy vector)
        :param q0: The default (resting state) joint configuration (1xN numpy vector)
        :param name: Name of the arm
        """
        self.num_links = links.size
        self.links = links
        self.q0 = q0
        self.name = name

        self.base = np.identity(4)
        self.tool = np.identity(4)

        # Set the arm to its default position
        self.reset()

    def update_link_angle(self, link, new_angle):
        """
        Updates the given link's angle with the given angle
        :param link: The link you want to update, given as a integer
        :param new_angle: The link's new angle
        """
        self.links[link].theta = new_angle


    def reset(self):
        """
        Resets the arm back to its resting state, i.e. q0
        """
        for link, q in zip(self.links, self.q0):
            link.set_theta(q)


    def fkine(self, q=None):
        """
        Computes the forward kinematics of the arm using the current joint
        configuration or a given joint configuration
        :param q: Optional joint configuration to compute the FK on (1xN numpy vector)
        """
        t = self.base
        for i, link in enumerate(self.links):
            if q:
                t = t* link.compute_transformation_matrix(q[i])
            else:
                t = t * link.transform_matrix
        t = t * self.tool
        return t

    def jacob0(self, q=None):
        """
        Calculates the jacobian in the world frame by finding it in the tool frame
        and then converting to the world frame
        :param q: Optional joint configuration to compute the jacobian on (1xN numpy vector)
        """
        J = self.jacobn(q)
        eet = self.fkine(q)
        rotation = utils.get_rotation_from_homogenous_transfrom(eet)
        zeros = np.zeros((3,3))
        a1 = np.hstack((rotation,zeros))
        a2 = np.hstack((zeros, rotation))
        J = np.vstack((a1,a2)) * J
        return J

    def jacobn(self, q=None):
        """
        Calculates the jacobian in the tool frame
        :param q: Optional joint configuration to compute the jacobian on (1xN numpy vector)
        """
        J = np.zeros((6, self.num_links))
        U = self.tool
        I = range(self.num_links-1,-1,-1)
        for i, link in zip(I, self.links[::-1]):
            if q:
                U = link.compute_transformation_matrix(q[i]) * U
            else:
                U = link.transform_matrix * U

            d = np.array([-U[0,0]*U[1,3]+U[1,0]*U[0,3],
                          -U[0,1]*U[1,3]+U[1,1]*U[0,3],
                          -U[0,2]*U[1,3]+U[1,2]*U[0,3]])
            delta = U[2,0:3]

            J[:,i] = np.vstack((d, delta)).flatten()
        return J
