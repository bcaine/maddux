"""
A stationary object that something may collide with.
"""
import numpy as np


class Target:

    def __init__(self, position, radius, angles=None, scores=None):
        """Target Init. Angles currently not used. The target is a sphere.

        :param position: 1x3 numpy array of position of center
        :param radius: radius of target
        :param angles: (Unused) - Angles of target with respect to x, y, and z axis.
        """
        self.position = position
        self.radius = radius
        # Currently not used
        self.angles = angles if angles else np.array([0, 90, 0])
        

    def get_score(self, position):
        """Given an object position hitting the target, return the score"""
        distance = np.linalg.norm(position - self.position)
        score = 0.75 ** distance
        return score if distance > self.radius else 10 * score
