"""
A stationary object that something may collide with.
"""
import numpy as np

HIT_ERROR = 0.01

class Target:

    def __init__(self, position, radius):
        """Target Init
        :param position: 1x3 numpy array of position of center
        :param radius: radius of target
        """
        self.position = np.array(position)
        self.radius = radius
        

    def get_score(self, position):
        """Given an object position hitting the target, return the score"""
        distance = np.linalg.norm(position - self.position)
        score = 0.75 ** distance
        return score if distance > self.radius else 10 * score


    def is_hit(self, ball):
        """Check if the target is hit.
        :param ball: A ball object
        """
        diff = np.absolute(ball.leading_point() - self.position)
        return diff[0] < self.radius and diff[1] < HIT_ERROR and diff[2] < self.radius


    def display(self):
        print "Position: {}".format(self.position)
        print "Radius: {}".format(self.radius)
