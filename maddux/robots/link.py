"""
A Link in a robot arm.
"""
import numpy as np

class Link:

    def __init__(self, theta, offset, length, twist, q_lim=None):
        """
        :param theta: Link angle, variable
        :param offset: Link offset, constant
        :param length: Link length, constant
        :param twist: Link twist, constant
        :param q_lim: Joint coordinate limits
        """
        self.offset = offset
        self.length = length
        self.twist = twist
        self.q_lim = q_lim
        self.set_theta(theta)

        
    def set_theta(self, theta):
        self.theta = theta
        self.transform_matrix = self.compute_transformation_matrix(theta)

        
    def compute_transformation_matrix(self, q):
        """
        Transformation matrix from the current theta to the new theta
        :param q: the new theta
        """
        sa = np.sin(self.twist)
        ca = np.cos(self.twist)
        st = np.sin(q)
        ct = np.cos(q)
        T = np.matrix([[ct, -st*ca, st*sa,  self.length*ct],
                       [st, ct*ca,  -ct*sa, self.length*st],
                       [0,  sa,     ca,     self.offset   ],
                       [0,  0,      0,      1             ]])
        return T

    
    def display(self):
        """
        Display the link's properties nicely
        """
        print 'Link angle: {}'.format(self.theta)
        print 'Link offset: {}'.format(self.offset)
        print 'Link length: {}'.format(self.length)
        print 'Link twist: {}'.format(self.twist)
