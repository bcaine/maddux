"""
A stationary object that something may collide with.
"""
import numpy as np


class Target:

    def __init__(self, position, radius, angles=None, scores=None):
        """Target Init

        :param position: 1x3 numpy array of position of center
        :param radius: radius of target
        :param angles: angles of target with respect to x, y, and z axis
        :param scores: a list of scores for each ring on the target
        """

        self.position = position
        self.radius = radius
        self.angles = angles if angles else np.array([0, 90, 0])
        self.scores = scores if scores else [50, 25, 10, 5, 2, 1]
        self.rings = np.linspace(0, radius, len(self.scores) + 1)[1:]


    def get_score(self, position):
        """Given an object position hitting the target, return the score"""
        distance = np.linalg.norm(position - self.position)

        if distance > self.radius:
            return 0
        
        for i, ring in enumerate(self.rings):
            if distance <= ring:
                return self.scores[i]
        return 0

    
