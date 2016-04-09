"""
A ball object to throw.
"""
import numpy as np
from throwable import ThrowableObject


class Ball(ThrowableObject):

    def __init__(self, position, radius):
        self.radius = radius
        self.name = "ball"
        ThrowableObject.__init__(self, position)
    

    def leading_point(self):
        """Return the outermost point on the y axis
           that will hit the target.
        """
        return self.position + np.array([0, self.radius, 0])
