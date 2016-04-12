"""
A ball object to throw.
"""
import numpy as np
from throwable import ThrowableObject
from maddux.utils.plot import plot_sphere


class Ball(ThrowableObject):

    def __init__(self, position, radius):
        self.radius = radius
        ThrowableObject.__init__(self, position)

    def leading_point(self):
        """Return the outermost point on the y axis
           that will hit the target.
        """
        return self.position + np.array([0, self.radius, 0])

    def plot(self, ax):
        """Plots the ball at its current location.

        :param ax: Figure to plot on.
        """
        return plot_sphere(self.position, self,radius, ax)
